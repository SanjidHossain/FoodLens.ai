import requests
from flask import Flask, render_template, request
from gradio_client import Client
import json
import pandas as pd

app = Flask(__name__)

client_origin = Client("https://sanjid-food-origin-classifier-distiltrobertabase.hf.space/")
client_ingredient = Client("https://sanjid-food-ingredient-classifier.hf.space/")


@app.route('/')
def Home():
    return render_template('home.html')

@app.route('/app', methods=['GET', 'POST'])
def app_route():
    label_list_origin = []
    is_empty_result_origin = True  # Flag to indicate if the origin result is empty

    label_list_ingredient = []
    is_empty_result_ingredient = True  # Flag to indicate if the ingredient result is empty

    if request.method == "POST":
        input_text = request.form['text']

        # Predict origin
        output_origin = predict_label_origin(input_text)[0]
        confident_list_origin = output_origin['confidences']
        for elem in confident_list_origin:
            if elem['confidence'] >= 0.4:
                is_empty_result_origin = False
                label_list_origin.append({
                    'label': elem['label'],
                    'confidence': int(elem['confidence'] * 100)
                })

        # Predict ingredient
        output_ingredient = predict_label_ingredient(input_text)[0]
        confident_list_ingredient = output_ingredient['confidences']
        for elem in confident_list_ingredient:
            if elem['confidence'] >= 0.5:
                is_empty_result_ingredient = False
                label_list_ingredient.append({
                    'label': elem['label'],
                    'confidence': int(elem['confidence'] * 100)
                })
    print(label_list_origin, is_empty_result_origin)
    return render_template('app.html',
                           label_list_origin=label_list_origin,
                           is_empty_result_origin=is_empty_result_origin,
                           label_list_ingredient=label_list_ingredient,
                           is_empty_result_ingredient=is_empty_result_ingredient)



def predict_label_origin(input_text):
    response = requests.post("https://sanjid-food-origin-classifier-distiltrobertabase.hf.space/run/predict", json={
        "data": [input_text]
    }).json()
    print(response)  # print the response
    data = response["data"]
    return data


def predict_label_ingredient(input_text):
    response = requests.post("https://sanjid-food-ingredient-classifier.hf.space/run/predict", json={
        "data": [input_text]
    }).json()
    data = response["data"]
    return data


csv_file_path = 'Data_for_image.csv'
df = pd.read_csv(csv_file_path)

api_name = ""  # Replace with the actual API name you intend to use.
gradio_client = Client("https://sanjid-food-classifier-resnet50.hf.space/" + ("/" + api_name if api_name else ""))

@app.route('/app2', methods=['GET', 'POST'])
def app2():
    if request.method == 'POST':
        # Get the uploaded image file
        image_file = request.files['image']

        if image_file:
            try:
                # Save the uploaded image temporarily (optional)
                temp_image_path = "temp_image.jpg"
                image_file.save(temp_image_path)

                # Provide the file path to the Gradio API
                result = gradio_client.predict(temp_image_path, api_name="/predict")
                print("Prediction Result File:", result)

                # Read the content of the JSON file
                with open(result, 'r') as json_file:
                    json_data = json.load(json_file)
                    top_label = json_data.get('label', 'Could not detect')
                    top_confidence = json_data.get('confidences', [])[0].get('confidence', 0)

                # Check if the top confidence is above 0.5
                if top_confidence > 0.5:
                    # Match the predicted food name with the CSV data
                    predicted_food_name = top_label
                    food_origin = get_food_origin_from_csv(predicted_food_name)
                    food_body = get_food_body_from_csv(predicted_food_name)

                    # Predict restrictive ingredient
                    output_ingredient = predict_label_ingredient(food_body)[0]
                    confident_list_ingredient = output_ingredient['confidences']
                    label_list_ingredient = []
                    for elem in confident_list_ingredient:
                        if elem['confidence'] >= 0.5:
                            label_list_ingredient.append({
                                'label': elem['label'],
                                'confidence': int(elem['confidence'] * 100)
                            })
                else:
                    food_origin = 'Could not detect'
                    label_list_ingredient = []

                # Add the 'predicted_food_name', 'food_origin', and 'label_list_ingredient' variables to the render_template call
                return render_template('app2.html', predicted_food_name=predicted_food_name, food_origin=food_origin, label_list_ingredient=label_list_ingredient)

            except Exception as e:
                print("Error:", str(e))

    # If the request method is not POST or there is no image, render the upload form
    return render_template('app2.html')


def get_food_body_from_csv(predicted_food_name):
    # Filter the DataFrame to find the row with matching food name
    matched_row = df[df['Name'] == predicted_food_name]

    if not matched_row.empty:
        # If a match is found, retrieve the "Body" value from the CSV
        food_body = matched_row.iloc[0]['Body']
    else:
        # If no match is found, set the body to "Not found" or handle it as needed
        food_body = 'Not found'

    return food_body


def get_food_origin_from_csv(predicted_food_name):
    # Filter the DataFrame to find the row with matching food name
    matched_row = df[df['Name'] == predicted_food_name]

    if not matched_row.empty:
        # If a match is found, retrieve the "Origin" value from the CSV
        food_origin = matched_row.iloc[0]['Origin']
    else:
        # If no match is found, set the origin to "Not found" or handle it as needed
        food_origin = 'Not found'

    return food_origin

@app.route('/about', methods=['GET', 'POST'])
def About():
    return render_template('about.html')



if __name__ == '__main__':
    app.run(debug=True)



