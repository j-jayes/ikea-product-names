import pandas as pd
from bs4 import BeautifulSoup
import requests


url = 'https://www.ikea.com/se/en/cat/furniture-fu001/?page=2'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
response = requests.get(url, headers=headers)
response.raise_for_status() # This will raise an error for non-200 status codes
html_content = response.text
# ----------------------------------------------------


# 1. Parse the HTML
# We use the 'lxml' parser for its speed and robustness.
soup = BeautifulSoup(html_content, 'lxml')

# 2. Find all product containers
# From our analysis, each product is within a 'div' with the class 'plp-mastercard'.
product_cards = soup.find_all('div', class_='plp-mastercard')

# 3. Loop and Extract Data
# We'll iterate through each product card and extract the desired information.
# A list of dictionaries is a great way to store structured data.
products_data = []
base_url = 'https://www.ikea.com'

for card in product_cards:
    product_info = {}

    # Using try-except blocks makes the scraper robust. If a piece of data
    # doesn't exist for one product, the script won't crash.
    try:
        # Extract the product name
        name_span = card.find('span', class_='plp-price-module__product-name')
        product_info['name'] = name_span.get_text(strip=True) if name_span else None

        # Extract the product description/details
        desc_span = card.find('span', class_='plp-price-module__description')
        product_info['description'] = desc_span.get_text(strip=True) if desc_span else None

        # Extract the price
        price_span = card.find('span', class_='plp-price__integer')
        if price_span:
            # Clean the price text: remove spaces and convert to a number (integer)
            price_cleaned = price_span.get_text(strip=True).replace(' ', '').replace(':-', '')
            product_info['price_sek'] = int(price_cleaned)
        else:
            product_info['price_sek'] = None
        
        # Extract the Product URL
        url_anchor = card.find('a', class_='plp-product__image-link')
        if url_anchor and url_anchor.has_attr('href'):
             product_info['product_url'] = base_url + url_anchor['href']
        else:
            product_info['product_url'] = None

        # Extract the main Image URL
        img_tag = card.find('img', class_='plp-product__image')
        if img_tag and img_tag.has_attr('src'):
             product_info['image_url'] = img_tag['src']
        else:
            product_info['image_url'] = None

        # Extract number of reviews
        rating_span = card.find('span', class_='plp-rating__label')
        if rating_span:
            # Clean the rating text to get only the number
            reviews_text = rating_span.get_text(strip=True).replace('(', '').replace(')', '')
            product_info['reviews_count'] = int(reviews_text)
        else:
            product_info['reviews_count'] = 0


    except Exception as e:
        print(f"An error occurred while parsing a product card: {e}")
        continue # Skip to the next product card

    products_data.append(product_info)

# 4. Structure data with Pandas
# Pandas DataFrames are perfect for analyzing and exporting structured data.
df = pd.DataFrame(products_data)

# 5. Display and Save the data
print("Successfully scraped the following data:")
print(df)

# Save the DataFrame to a CSV file for future use.
# index=False prevents pandas from writing row indices into the CSV.
df.to_csv('ikea_furniture.csv', index=False, encoding='utf-8')

print("\nData has been saved to ikea_furniture.csv")