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


# URL to scrape
url = 'https://www.allrecipes.com/cuisine-a-z-6740455'

# Function to scrape and save URLs to a CSV file
def scrape_and_save_urls(url):
    driver.get(url)
    time.sleep(2)

    # Create a list to store the data
    data = []

    # Find and iterate through the links
    links = driver.find_elements(By.XPATH, '//li[starts-with(@id, "link-list__item_1-0")]')
    for link in links:
        name = link.text
        url = link.find_element(By.XPATH, './a').get_attribute('href')
        data.append({'Name': name, 'URL': url})

    # Create a DataFrame
    df = pd.DataFrame(data)

    # Save the data to a CSV file
    df.to_csv('recipe_urls.csv', index=False)

    print("URLs saved to 'recipe_urls.csv'")

# Call the function to scrape and save the URLs
scrape_and_save_urls(url)

# Close the webdriver
driver.quit()
