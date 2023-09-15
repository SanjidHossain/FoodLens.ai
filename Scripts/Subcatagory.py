from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import time

# Create an instance of Options
options = Options()

# Initialize the Edge webdriver
service = Service(EdgeChromiumDriverManager().install())
driver = webdriver.Edge(service=service, options=options)

# Create a list to store the scraped data
scraped_data = []

# Function to scrape and save data
def scrape_and_save_data(url):
    driver.get(url)
    time.sleep(2)

    # Check if the page contains the desired elements
    name_element = driver.find_element(By.XPATH, "//h1[@id='mntl-taxonomysc-heading_1-0']")
    taxonomy_elements = driver.find_elements(By.XPATH, "//a[starts-with(@id, 'taxonomy-nodes__link_1-0')]")

    if name_element and taxonomy_elements:
        name = name_element.text

        for element in taxonomy_elements:
            url = element.get_attribute('href')
            scraped_data.append({'Name': name, 'URL': url})

# Read the URLs from the CSV file 'recipe_urls.csv'
df = pd.read_csv('recipe_urls.csv')

# Iterate through the URLs and scrape data
for _, row in df.iterrows():
    url = row['URL']
    scrape_and_save_data(url)

# Create a DataFrame from the scraped data
scraped_df = pd.DataFrame(scraped_data)

# Save the scraped data to a CSV file
scraped_df.to_csv('sub_data.csv', index=False)

# Close the webdriver
driver.quit()
