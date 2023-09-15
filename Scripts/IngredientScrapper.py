from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Initialize the Edge webdriver
driver = webdriver.Edge()

# Create a list to store the scraped data
scraped_data = []

# Function to scrape and save data
def scrape_and_save_data(url, origin):
    try:
        driver.get(url)

        # Wait for the element to be present (adjust timeout as needed)
        wait = WebDriverWait(driver, 10)
        name_element = wait.until(EC.presence_of_element_located((By.XPATH, "//h1[@id='article-heading_1-0']")))

        name = name_element.text

        # Scrape Description
        description_element = driver.find_element(By.XPATH, "//p[@id='article-subheading_1-0']")
        description = description_element.text

        # Scrape Ingredients
        ingredients_elements = driver.find_elements(By.XPATH, "//ul[@class='mntl-structured-ingredients__list']//li")
        ingredients = [ingredient.text for ingredient in ingredients_elements]

        # Append the scraped data to the list
        scraped_data.append({'Name': name, 'Description': description, 'Recipe': ingredients, 'Origin': origin, 'URL': url})
    except Exception as e:
        print(f"Error scraping URL: {url}")
        print(e)

# Read the Origin and URL data from the CSV file 'scraped_data.csv'
df = pd.read_csv('scraped_data.csv')

# Iterate through the URLs and scrape data
for _, row in df.iterrows():
    url = row['URL'] 
    origin = row['Origin']
    scrape_and_save_data(url, origin)

# Create a DataFrame from the scraped data
scraped_df = pd.DataFrame(scraped_data)

# Save the scraped data to a CSV file
scraped_df.to_csv('scraped_data_updated.csv', index=False)

# Close the webdriver
driver.quit()
