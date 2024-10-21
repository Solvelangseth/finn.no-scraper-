from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import time

# Set the correct path to GeckoDriver (for Firefox)
service = Service('/Users/solvelangseth/Documents/finn_prosjekt/ScrapeFinnBolig/geckodriver')

# Set Firefox options for headless mode
options = Options()
options.headless = True  # Run Firefox in headless mode

# Start the WebDriver with Firefox in headless mode
driver = webdriver.Firefox(service=service, options=options)

# Base URL for the search query (adjust the query as needed)
base_url = "https://www.finn.no/bap/forsale/search.html?q=game+boy&page="

# Number of pages to scrape
num_pages = 5

# List to store product data
product_data = []

# Iterate over the first 5 pages of search results
for page_num in range(1, num_pages + 1):
    # Build the URL for the current page
    search_results_url = base_url + str(page_num)
    
    # Visit the search results page
    driver.get(search_results_url)
    time.sleep(3)  # Delay to allow the page to load fully

    # Extract all product links on the page
    product_elements = driver.find_elements(By.CSS_SELECTOR, 'a.sf-search-ad-link')
    product_urls = [element.get_attribute('href') for element in product_elements if element.get_attribute('href')]

    print(f"Found {len(product_urls)} products on page {page_num}.")

    # Iterate over each product URL and scrape the data with a delay between requests
    for product_url in product_urls:
        driver.get(product_url)
        time.sleep(3)  # Delay between scraping each product page

        # Extract title
        try:
            title = driver.find_element(By.TAG_NAME, 'h1').text
        except:
            title = 'No title'

        # Extract price from shadow DOM
        try:
            shadow_host = driver.find_element(By.CSS_SELECTOR, 'tjt-podlet-create-offer-button-isolated')
            shadow_root = driver.execute_script('return arguments[0].shadowRoot', shadow_host)
            price = shadow_root.find_element(By.CLASS_NAME, 'h2').text
        except:
            price = 'No price available'

        # Extract description
        try:
            description = driver.find_element(By.CLASS_NAME, 'whitespace-pre-wrap').text
        except:
            description = 'No description'

        # Extract condition
        try:
            condition = driver.find_element(By.CSS_SELECTOR, 'p.mb-0 b').text
        except:
            condition = 'No condition'

        # Append the data to the list
        product_data.append({
            'URL': product_url,
            'Title': title,
            'Price': price,
            'Description': description,
            'Condition': condition
        })

    print(f"Completed scraping page {page_num}.")

# Close the browser after scraping all pages
driver.quit()

# Convert the product data into a Pandas DataFrame for better visualization
df = pd.DataFrame(product_data)

# Print the DataFrame (optional)
print(df)

# Save the data to a CSV file
df.to_csv('/Users/solvelangseth/Documents/finn_prosjekt/finn_product_details_gameboy.csv', index=False)

# Let the user know the scraping is complete
print("Scraping complete. Data saved to CSV.")
