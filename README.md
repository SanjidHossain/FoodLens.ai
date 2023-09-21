# FoodLens.ai

<img src = "https://github.com/SanjidHossain/FoodLens.ai/blob/main/Deployments/Web%20application/FOODLENS.ai.png" width="1000" height="300">

A Web application that can detect food, Ingredients and origin from both text and image. The application is built from data collection, model training, and deployment that can classify Foods. <br/>
The model can classify 239 different foods from images as well as detect the Origins of the food and Restrictive Ingredients(Allergies, Dairy, Meat, etc.) from description of any food.

###  Visit the [website Here !!](https://foodlens-ai.onrender.com/)

 ## Data Collection

 ### Text Data

Data was collected from Website of [AllRecipes](https://www.allrecipes.com/) and `5780` Food Recipes were scraped <br/>The data collection was completed in 2 steps:

 - **Step-1:- Food URL Scraping:** The URLs of foods were scraped with `Scripts\URLScrapper.py` and the URLs are stored along with food names in `Data\Text Data\scraped_data.csv`
 - **Step2:- Food Recipe Scraping:** Using the URLs, Food Name, Description, and Food Recipe are scraped with `Scripts\IngredientScrapper.py` and they are stored in `Data\Text Data\Dataset(final).csv`

 ### Image Data

 Image Data was collected 2 ways<\br>

 Two popular Image Datasets were taken From Kaggle:
  - [FOOD 101:](https://www.kaggle.com/datasets/dansbecker/food-101) that consisted Images of 101 popular foods(1000 images per foods) around the world.
  - [Indian Food Images Dataset:](https://www.kaggle.com/datasets/iamsouravbanerjee/indian-food-images-dataset) that consisted 80 popular food of India(50 Images per food). <br/>

 Secondly, 58 popular food dishes(170 images per food) from Some of the popular traveling destinations of European and Asian countries were also scraped with DuckDuckGo search using their term name.

## Data Preprocessing

Initially, The collected data only contained Description, Origin, and Recipes. However, the Resrticitve ingredient list was created with brief research on foods and Recipes and based on some of the most common and popular ingredients that are used in food and their recipes. 11 Restrictive groups were created based on the food or ingredients that are restricted against the groups`Non-vegan`, `dairy`, `Non-Vegetarian`, `Non-Pescatarian`, `Meat`, `Haram`, `Nut-allergies`, `pork`, `beef`, `alcohol`, `Sea-foods`. Using NLTK tools for keyword detection was used on some common keywords and ingredients during preprocessing. During preprocessing some of the data were dropped and the final dataset for the Restrictive group was `4834`.<\br>

As for Image data, the scraped data were manually checked and Cleaned.

### Data augmentation
While Food 101 Dataset had balanced 1000 images per class, the rest of the classes had comparatively less image data. to balanced the data we used Image augmentation(`Scripts\ImageAug.py`) to increase the data size for both Indian image data and scrapped data, the images were augmented in multiple layers to reach 950 to 1000 images per class.

## Model Training

### NLP(Restrcitive-Ingredient)

For model selection of Restrictive food Ingredient detection Model, a `distilrobera-base` model from HuggingFace Transformers was finetuned that uses Fastai and Blurr. The model training notebook can be viewed at `Notebooks\Food-Restriction\Food_Restriction.ipynb`

#### Benchnarking
| Model             | train_loss    | valid_loss        | accuracy_multi   | Model Size    |
| -------------     | ------------- | -------------     | -------------    | ------------- |
| roberta-base      | 0.050930      | 0.042578          |  98.19%          | 480 MB        |
| distilrobera-base | 0.057865      | 0.045424	        |  98.28%          | 322 MB        |

Since, they had nearly similar results, while model size was more compact for `distilrobera-base` this was selected. The F1 Score (Micro) = 96.50% &
F1 Score (Macro) = 94%

### NLP(Food-Origin)

For model selection of Food Origin detection Model, a `distilrobera-base` model from HuggingFace Transformers was finetuned that uses Fastai and Blurr. The model training notebook can be viewed at `Notebooks\Food-Origin\Food_origin.ipynb`

#### Benchnarking
| Model             | train_loss    | valid_loss        | accuracy_multi   | Model Size    |
| -------------     | ------------- | -------------     | -------------    | ------------- |
| roberta-base      | 0.040012      | 0.037279          |  98.4%           | 480 MB        |
| distilrobera-base | 0.048786	    | 0.044740          |  98.3%           | 322 MB        |

Since, distilrobera-base demonstrated 3% better result while also being more compact size wise. `distilrobera-base` was selected. The F1 Score (Micro) = 92.50% &
F1 Score (Macro) = 90%

### Image(Food-Detection)

For model selection of Image classification Model, `Resnet-50` model from HuggingFace Transformers was finetuned that uses Fastai and Blurr. The model training notebook can be viewed at `Notebooks\Food-Detection(Image)\Image.ipynb`

#### Benchnarking
| Model             | train_loss    | valid_loss        | error_rate	   | accuracy      |
| -------------     | ------------- | -------------     | -------------    | ------------- |
| Resnet-34         | 0.416365      | 0.388924          |  0.100993        | 89.90%        |
| Resnet-50         | 0.337102      | 0.318108          |  0.083765        | 91.62%        |

Since, Resnet-50 demonstrated 2% better result Despite being a more complex model. `Resnet-50` was selected

## Model Compression and ONNX Inference

The trained NLP model has a memory of 322+MB. For better usage, the model was compressed using ONNX quantization and brought under 82MB.

## Model Deployment

All three of the model is deployed to HuggingFace Spaces Gradio App. The implementation can be found in `deployment` folder
[Visit here](https://huggingface.co/spaces/sanjid/Food-ingredient-Classifier) to checkout the NLP Model for Restricitve Ingredient classfier


<img src = "https://github.com/SanjidHossain/FoodLens.ai/blob/main/Deployments/Food%20Ingredient%20Classifier/app.png" width="800" height="400">
<br/>

[Visit here](https://huggingface.co/spaces/sanjid/Food-classifier-Resnet50) to checkout the image model
<img src = "https://github.com/SanjidHossain/FoodLens.ai/blob/main/Deployments/Food-classifier-Resnet50/app.png" width="800" height="400">
<br/>

[Visit here](https://huggingface.co/spaces/sanjid/Food-Origin-classifier-distiltrobertabase) to checkout the NLP Model for Origin classfier
<img src = "https://github.com/SanjidHossain/FoodLens.ai/blob/main/Deployments/Food%20Origin%20classifier/oiriginapi.png" width="800" height="400">
<br/>

## Web Deployment
A Flask App has been built and published on `render`. The web app can take any form of News or article and show the Category or type of the article as output. Check `flask ` branch.
**Please visit the [Website](https://foodlens-ai.onrender.com/)**

### Home Page:
<img src = "https://github.com/SanjidHossain/FoodLens.ai/blob/main/Deployments/Web%20application/Home.png" width="800" height="400">
<br/>

### Culinary Insights:
<img src = "https://github.com/SanjidHossain/FoodLens.ai/blob/main/Deployments/Web%20application/textapp.png" width="800" height="400">
<br/>

### SnapPlate:
<img src = "https://github.com/SanjidHossain/FoodLens.ai/blob/main/Deployments/Web%20application/imageapp.png" width="800" height="400">
<br/>

### About:
<img src = "https://github.com/SanjidHossain/FoodLens.ai/blob/main/Deployments/Web%20application/About.png" width="800" height="400">
<br/>

