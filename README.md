# FoodLens.ai

# FoodLens.ai

A Web application that can detect food, Ingredients and origin from both text and image. The application is built from data collection, model training, and deployment that can classify Foods. <br/>
The model can classify 239 different foods from images as well as detect the Origins of the food and Restrictive Ingredients(Allergies, Dairy, Meat, etc.) from description of any food.

###  Visit the [website Here !!]()

 ## Data Collection

 ### Text Data

Data was collected from Website of [AllRecipes](https://www.allrecipes.com/) and `5780` Food Recipes were scraped <br/>The data collection was completed in 2 steps:

 - **Step-1:- Food URL Scraping:** The URLs of foods were scraped with `Scripts\URLScrapper.py` and the URLs are stored along with food names in `Data\Text Data\scraped_data.csv`
 - **Step2:- Food Recipe Scraping:** Using the URLs, Food Name, Description, and Food Recipe are scraped with `Scripts\IngredientScrapper.py` and they are stored in `Data\Text Data\Dataset(final).csv`

 ### Image Data

 Image Data was collected 2 ways<\br>

 Two popular Image Dataset were taken From Kaggle:
  - [FOOD 101:](https://www.kaggle.com/datasets/dansbecker/food-101) that consisted Images of 101 popular foods(1000 images per foods) around the world.
  - [Indian Food Images Dataset:](https://www.kaggle.com/datasets/iamsouravbanerjee/indian-food-images-dataset) that consisted 80 popular food of India(50 Images per food). <\br>

 Secondly, 58 popular food dishes(170 images per food) from Some of the poplar traveling destinations of European and Asian countries were also scraped with DuckDuckGo search using their term name.

## Data Preprocessing

Initially, The collected data only contained Description, Origin, and Recipes. However, the Resrticitve ingredient list was created with brief research on foods and Recipes and based on some of the most common and popular ingredients that are used in food and their recipes. 11 Restrictive groups were created based on the food or ingredients that are restricted against the groups`Non-vegan`, `dairy`, `Non-Vegetarian`, `Non-Pescatarian`, `Meat`, `Haram`, `Nut-allergies`, `pork`, `beef`, `alcohol`, `Sea-foods`. Using NLTK tools for keyword detection was used on some common keywords and ingredients during preprocessing. However during preprocessing none of the data were dropped as there were no null values.<\br>

As for Image data, the scraped data were manually checked and Cleaned.

### Data augmentation

#### Image Augmentation:
While Food 101 Dataset had balanced 1000 images per class, the rest of the classes had comparatively less image data. to balanced the data we used Image augmentation(`Scripts\ImageAug.py`) to increase the data size for both Indian image data and scrapped data, the images were augmentated in multiple layers to reach 950 to 1000 images per class.


## Model Training

For model selection, a `distilrobera-base` model from HuggingFace Transformers was finetuned that uses Fastai and Blurr. The model training notebook can be viewed [here](https://github.com/SanjidHossain/Multilabel-News-Classifier/blob/main/Notebooks/Blurr_Onnx.ipynb)

## Model Compression and ONNX Inference

The trained model has a memory of 322+MB. For better usage, the model was compressed using ONNX quantization and brought under 82MB.

## Model Deployment

The compressed model is deployed to HuggingFace Spaces Gradio App. The implementation can be found in `deployment` folder or [here](https://huggingface.co/spaces/sanjid/News_Classifier)

<img src = "https://github.com/SanjidHossain/Multilabel-News-Classifier/blob/main/Data/Image%20sources/app_gradio.png" width="800" height="400">

## Web Deployment
A Flask App has been built and published on `render`. The web app can take any form of News or article and show the Category or type of the article as output. Check `flask ` branch.
**Please visit the [Website](https://multilab-news-classifier.onrender.com)**

<img src = "Data/Image sources/Web_app.png" width="800" height="400">


