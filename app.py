import requests
from flask import Flask, render_template, request
from gradio_client import Client
import json

app = Flask(__name__)

client_origin = Client("https://sanjid-food-origin-classifier-distiltrobertabase.hf.space/")
client_ingredient = Client("https://sanjid-food-ingredient-classifier.hf.space/")

@app.route('/')
def Home():
    return render_template('home.html')

@app.route('/app', methods=['GET', 'POST'])
def app_route():  # Renamed from 'app' to 'app_route'
    label_list_origin = []
    is_empty_result = True  # Flag to indicate if the result is empty

    if request.method == "POST":
        output = predict_label(request.form['text'])[0]
        confident_list = output['confidences']
        for elem in confident_list:
            if elem['confidence'] >= 0.6:
                is_empty_result = False # Update flag if result is found
                label_list_origin.append({
                    'label': elem['label'],
                    'confidence': int(elem['confidence'] * 100)
                })

    return render_template('app.html', label_list=label_list_origin, is_empty_result=is_empty_result)

def predict_label(input_text):
    response = requests.post("https://sanjid-food-origin-classifier-distiltrobertabase.hf.space/run/predict", json={
        "data": [
            input_text
        ]
    }).json()
    data = response["data"]
    return data

@app.route('/app2', methods=['GET', 'POST'])
def app2():
    return render_template('app2.html')

@app.route('/about', methods=['GET', 'POST'])
def About():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
