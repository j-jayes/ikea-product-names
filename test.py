import requests
from bs4 import BeautifulSoup
import json

# The URL of the IKEA products page
url = "https://www.ikea.com/se/en/cat/beds-bm003/?page=2"

# Send a GET request to the URL
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all the product containers
    product_cards = soup.find_all('div', class_='plp-mastercard')

    # A list to hold the extracted product information
    products_data = []

    # Loop through each product card and extract the information
    for card in product_cards:
        try:
            product_name = card.find('span', class_='plp-price-module__product-name').text.strip()
            product_description = card.find('span', class_='plp-price-module__description').text.strip()
            price = card.find('span', class_='plp-price__integer').text.strip()
            currency = card.find('span', class_='plp-price__currency').text.strip()
            product_url = card.find('a', class_='plp-product__image-link')['href']
            image_url = card.find('img', class_='plp-image')['src']

            # Extract rating if available
            rating_element = card.find('span', class_='plp-rating__label')
            rating = rating_element.text.strip() if rating_element else 'N/A'

            product_info = {
                'name': product_name,
                'description': product_description,
                'price': f"{price}{currency}",
                'url': product_url,
                'image_url': image_url,
                'rating': rating
            }
            products_data.append(product_info)
        except AttributeError:
            # Skip if a product card is missing some information
            continue

    # Print the extracted data as a JSON object
    print(json.dumps(products_data, indent=4))

else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")