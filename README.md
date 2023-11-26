# FoodLens.ai

<img src = "https://github.com/SanjidHossain/FoodLens.ai/blob/main/Deployments/Web%20application/FOODLENS.ai.png" width="1000" height="300">

A Web application that can detect food, Ingredients and origin from both text and image. The application is built from data collection, model training, and deployment that can classify Foods. <br/>
The model can classify 239 different foods from images as well as detect the Origins of the food and Restrictive Ingredients(Allergies, Dairy, Meat, etc.) from description of any food.
## Project Overview:

[Data Managment](#point1): Data collection,Preprocessing and Augmentation.<br/>
[ML Model](#point2): Model Training, Benchmarking and Compression .<br/>
[API](#point3): Model Deployment and API building .<br/>
[Application](#point4): API integration and Web application Development.<br/>
[Future Updates:](#point5): Plans and Future Updates.<br/>

###  Visit the [website Here !!](https://foodlens-ai.onrender.com/)

<a id="point1"></a>
 ## Data Collection

 ### Text Data

Data was collected from Website of [AllRecipes](https://www.allrecipes.com/) and `5780` Food Recipes were scraped <br/>The data collection was completed in 2 steps:

 - **Step-1:- Food URL Scraping:** The URLs of foods were scraped with `Scripts\URLScrapper.py` and the URLs are stored along with food names in `Data\Text Data\scraped_data.csv`
 - **Step2:- Food Recipe Scraping:** Using the URLs, Food Name, Description, and Food Recipe are scraped with `Scripts\IngredientScrapper.py` and they are stored in `Data\Text Data\Dataset(final).csv`

 ### Image Data

 Image Data was collected 2 ways <br/>

 Two popular Image Datasets were taken From Kaggle:
  - [FOOD 101:](https://www.kaggle.com/datasets/dansbecker/food-101) that consisted Images of 101 popular foods(1000 images per foods) around the world.
  - [Indian Food Images Dataset:](https://www.kaggle.com/datasets/iamsouravbanerjee/indian-food-images-dataset) that consisted 80 popular food of India(50 Images per food). <br/>

 Secondly, 58 popular food dishes(170 images per food) from Some of the popular traveling destinations of European and Asian countries were also scraped with DuckDuckGo search using their term name.

## Data Preprocessing

Initially, The collected data only contained Description, Origin, and Recipes. However, the Resrticitve ingredient list was created with brief research on foods and Recipes and based on some of the most common and popular ingredients that are used in food and their recipes. 11 Restrictive groups were created based on the food or ingredients that are restricted against the groups`Non-vegan`, `dairy`, `Non-Vegetarian`, `Non-Pescatarian`, `Meat`, `Haram`, `Nut-allergies`, `pork`, `beef`, `alcohol`, `Sea-foods`. Using NLTK tools for keyword detection was used on some common keywords and ingredients during preprocessing. During preprocessing some of the data were dropped and the final dataset for the Restrictive group was `4834`.<\br>

As for Image data, the scraped data were manually checked and Cleaned.


## Data augmentation

### Image Data augmentation
While Food 101 Dataset had balanced 1000 images per class, the rest of the classes had comparatively less image data. to balance the data we used Image augmentation(`Scripts\ImageAug.py`) to increase the data size for both Indian image data and scrapped data, the images were augmented in multiple layers to reach 950 to 1000 images per class. <br/>

### Text data augmentation
While 4834 data was working well for Restrictive Ingredient classification, it was different for Origin classification as in most cases origins tend to be single-label, so more data was necessary for better results and to increase the data size NLTK tool was used for text augmentation and the data was increased to more than `21,000` where each of the class had at least `600` data.
<br/>

All the Data for all three of the models has been linked and stored in the `Data` directory

<a id="point2"></a>

## Model Training

### NLP(Restrcitive-Ingredient)

For the model selection of the Restrictive food Ingredient detection Model, a `distilrobera-base` model from HuggingFace Transformers was finetuned that uses Fastai and Blurr. The model training notebook can be viewed at `Notebooks\Food-Restriction\Food_Restriction.ipynb`

#### Benchmarking
| Model             | train_loss    | valid_loss        | accuracy_multi   | Model Size    |
| -------------     | ------------- | -------------     | -------------    | ------------- |
| roberta-base      | 0.050930      | 0.042578          |  98.19%          | 480 MB        |
| distilrobera-base | 0.057865      | 0.045424	        |  98.28%          | 322 MB        |

Since, they had nearly similar results, while the model size was more compact for `distilrobera-base` this was selected. The F1 Score (Micro) = 96.50% &
F1 Score (Macro) = 94%

### NLP(Food-Origin)

For the model selection of the Food Origin detection Model, a `distilrobera-base` model from HuggingFace Transformers was finetuned that uses Fastai and Blurr. The model training notebook can be viewed at `Notebooks\Food-Origin\Food_origin.ipynb`

#### Benchmarking
| Model             | train_loss    | valid_loss        | accuracy_multi   | Model Size    |
| -------------     | ------------- | -------------     | -------------    | ------------- |
| roberta-base      | 0.040012      | 0.037279          |  98.4%           | 480 MB        |
| distilrobera-base | 0.048786	    | 0.044740          |  98.3%           | 322 MB        |

Since both models demonstrated similar results while distilrobera was more compact size-wise. `distilrobera-base` was selected. The F1 Score (Micro) = 72% and F1 Score (Macro) = 0.69%

### Image(Food-Detection)

For the model selection of the Image classification Model, `Resnet-50` model from HuggingFace Transformers was finetuned using Fastai and Blurr. The model training notebook can be viewed at `Notebooks\Food-Detection(Image)\Image.ipynb`

#### Benchmarking
| Model             | train_loss    | valid_loss        | error_rate	   | accuracy      |
| -------------     | ------------- | -------------     | -------------    | ------------- |
| Resnet-34         | 0.416365      | 0.388924          |  0.100993        | 89.90%        |
| Resnet-50         | 0.337102      | 0.318108          |  0.083765        | 91.62%        |

Since Resnet-50 demonstrated a 2% better result Despite being a more complex model. `Resnet-50` was selected

## Model Compression and ONNX Inference

The trained NLP model has a memory of 322+MB. For better usage, the model was compressed using ONNX quantization and brought under 82MB for both Restrictive Ingredient Model and Origin classification Model.

<a id="point3"></a>
## Model Deployment

<a id="Api1"></a>
All three of the model is deployed to HuggingFace Spaces `Gradio` App. The implementation can be found in `deployment` folder
[Visit here](https://huggingface.co/spaces/sanjid/Food-ingredient-Classifier) to check the NLP Model for Restrictive Ingredient classifier


<img src = "https://github.com/SanjidHossain/FoodLens.ai/blob/main/Deployments/Food%20Ingredient%20Classifier/app.png" width="800" height="400">
<br/>

<a id="Api2"></a>
[Visit here](https://huggingface.co/spaces/sanjid/Food-classifier-Resnet50) to check out the image model
<img src = "https://github.com/SanjidHossain/FoodLens.ai/blob/main/Deployments/Food-classifier-Resnet50/app.png" width="800" height="400">
<br/>

<a id="Api3"></a>
[Visit here](https://huggingface.co/spaces/sanjid/Food-Origin-classifier-distiltrobertabase) to check the NLP Model for the Origin classifier
<img src = "https://github.com/SanjidHossain/FoodLens.ai/blob/main/Deployments/Food%20Origin%20classifier/oiriginapi.png" width="800" height="400">
<br/>


<a id="point4"></a>
## Web Deployment
A Flask App has been built and published on `render`. The web app can take any form of News or article and show the Category or type of the article as output. Check `flask ` branch.
**Please visit the [Website](https://foodlens-ai.onrender.com/)**

### Home Page:
<img src = "https://github.com/SanjidHossain/FoodLens.ai/blob/main/Deployments/Web%20application/Home.png" width="800" height="400">
<br/>

Background Image used in the `Homepage` was specifically generated from [Leaonardo.ai](https://leonardo.ai/) based on the theme of this web application. <br\>
Home-Page consists of Navigation pannel With option to access (`Home`,`Culinary Insight`,`SnapPlate:Food detective`,`About`) and 2 main Feature of the application.<br\>

- **Culinary Insight:** This is linked to the NLP application of the website and sends `Culinary Insight` application
- **SnapPlate:Food Detective** This is linked to Image Recognition application of the website and Opens `SnapPlate:Food detective` application
  

### Culinary Insights:
<img src = "https://github.com/SanjidHossain/FoodLens.ai/blob/main/Deployments/Web%20application/textapp.png" width="800" height="400">
<br/>

Background Image used in the `Culinary Insight` was specifically generated from [Leaonardo.ai](https://leonardo.ai/) based on the theme of this web application. <br/>
Culinary Insight consists of Navigation pannel With option to access (`Home`,`Culinary Insight`,`SnapPlate:Food detective`,`About`) and The main application of the page. <br/>
The application Takes text data from user and provide results based on the data. <br/>

- **Input-Box:** Input Box holds the texts data for the application to recieve.
- **Speech:** This button enables the speech-to-text option from browser using js function. the text from this feature is directly utilized and can be visible in `Input-box`.
- **Submit:** This Button post the form that consists of text data in `input-box` to APIs in back end
- **Origin:** This Container demonstrates the origin of the food based on the text data from User. The result in this container directly comes from the food [origin classification](#Api3) API deoployed in hugging face
- **Restricitve-Ingredient:** This Container demonstrates the Restrictive-ingredients(Pork,Beef,alcohol,nuts etc.) of the food based on the text data from User. The result in this container directly comes from the [Restrictive-Ingredient classification](#Api1) API deoployed in hugging face.
- **Clear:** Clear button clears both texts and the all the results in the application for new action. 



### SnapPlate:
<img src = "https://github.com/SanjidHossain/FoodLens.ai/blob/main/Deployments/Web%20application/imageapp.png" width="800" height="400">
<br/>

Background Image used in the `SnapPlate:Food detective` was the same AI generated image used in `Culinary Insight` page . <br/>
SnapPlate:Food detective consists of Navigation pannel With option to access (`Home`,`Culinary Insight`,`SnapPlate:Food detective`,`About`) and The main application of the page.<br/>
The application Takes Image data from user and provide the results based on the data. <br/>

- **Browse Image:** Image browsing or captur image option, takes the image from users
- **Submit:** Submit option sends the Image that is caputured or selected through browsing in device and send the Image to API and Receive the Results based on user input
- **Food Name:** Demonstrates the Food name taken in result by  Using Image, application sends the image to [Food Classifier](#Api2) API deployed in hugging face. The API returns the Name of the user back to aplication. For each food a description has been already created and set up in backend.
- **Food Origin:** Based on Food name and the description set up for the food, Data is sent to [origin classification](#Api3) and recieve the data from the api and posted in results
- **Restrictive-Ingredient:** Based on Food name and the description set up for the food, Data is sent to [Restrictive-Ingredient classification](#Api1) and recieve the data from the api and posted in results
- **Show-Image:** This option enable users to view the subject/image that the result is based on or was selected for submission
- **Clear:** Clear button clears the Image and the Results for next submission.

### About:
<img src = "https://github.com/SanjidHossain/FoodLens.ai/blob/main/Deployments/Web%20application/About.png" width="800" height="400">
<br/>

Background Image used in the `About` was the same AI generated image used in `Culinary Insight` page . <br/>
About of Navigation pannel With option to access (`Home`,`Culinary Insight`,`SnapPlate:Food detective`,`About`) and The main container with a message.<br/>

The Page consists a container with message from Developers that contains information regarding the application and development process.<br/> 

The other feature of this page is a `Footer` that is consists of 2 options.

- **LinkedIn:** Link to the LinkedIn profile of the Developer of web application
- **Github:** Link to the Github profile of the Developer of web application


<a id="point5"></a>
## Updates:
The Web application is currently Live and working well with both Image and text data. Two Major updates are in plan and in development and long-term improvement is in plan. They will be added very soon

  -  **Image Scanner: Version: 0.1.1**
    <br/>
    In this update, we are excited to introduce a new feature to our application: the Image Scanner. This feature allows users to scan images from food packaging and menus and provides relevant results based on the scanned image. By leveraging image
    recognition technology, users can easily obtain information about various food items.

  -  **Multilingual Support: Version: 0.1.2**
    <br/>
    Building upon the Image Scanner, our next plan is to introduce a Multilingual update. This feature will enable the app to scan food descriptions, menus, and packaging containing different languages. Users will be able to translate and understand the
    content in their preferred language, enhancing the usability and accessibility of the application.


  -  **Long-term Plan: Image Model Update**
    <br/>
    As part of our long-term vision, we aim to continuously improve the accuracy and scope of our image recognition capabilities. We have plans to expand and enhance the image model by incorporating additional subjects and dishes. This update will result in
    more precise and comprehensive results, further enhancing the user experience.


***Thank you for your continued support, and we look forward to bringing you more exciting features and updates in the future.***
