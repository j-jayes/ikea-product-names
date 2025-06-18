import marimo

__generated_with = "0.13.15"
app = marimo.App(width="medium")


@app.cell
def _():
    import requests
    import re
    import time
    import pandas as pd
    from bs4 import BeautifulSoup
    from urllib.parse import urljoin

    # This function remains the same, as we still need to get the category
    # from the individual product HTML page.
    def get_full_category_path(product_page_html):
        """Parses the HTML of a product page to find the full breadcrumb category path."""
        if not product_page_html:
            return []
    
        product_soup = BeautifulSoup(product_page_html, 'lxml')
    
        breadcrumb_list = product_soup.find('ol', class_='bc-breadcrumb__list')
        if not breadcrumb_list:
            return []
    
        category_links = breadcrumb_list.find_all('a', class_='bc-breadcrumb__link')
    
        if category_links:
            full_path = [link.get_text(strip=True) for link in category_links]
            return full_path
    
        return []

    def scrape_ikea_beds_api():
        """
        Scrapes product information for all beds from the IKEA Sweden website
        by calling their internal JSON API and handling pagination.

        Returns:
            list: A list of dictionaries, where each dictionary contains the
                  information for a single product.
        """
    
        # The API endpoint identified from the HAR file
        api_url = "https://www.ikea.com/se/en/plp-range-facade/api/search"
        all_products = []
        current_page = 1
    
        # Headers to mimic a browser request
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        print("Starting the API scraping process...")

        while True:
            # Parameters for the API request
            params = {
                "query": "*",
                "sort": "RELEVANCE",
                "page": current_page,
                "size": 24, # The number of items per page
                "catalog": "bm003", # The category ID for Beds
                "market": "se/en"
            }

            try:
                print(f"Scraping API page: {current_page}")
                # Stage 1: Fetch data from the API
                response = requests.get(api_url, params=params, headers=headers, timeout=15)
                response.raise_for_status()
            
                data = response.json()
            
                # The actual product list is inside the 'products' key
                products_on_page = data.get("products", [])

                # If the product list is empty, we've reached the end
                if not products_on_page:
                    print("No more products found in API response. Ending pagination.")
                    break

                # Process each product from the JSON response
                for product in products_on_page:
                    product_data = {}

                    # --- Extract data directly from the JSON response ---
                    product_data['name'] = product.get('name')
                    product_data['price'] = product.get('price', {}).get('value')
                
                    full_description = product.get('description')
                    product_data['url'] = product.get('url')

                    # Use regex to separate the description from the dimensions
                    dimension_match = re.search(r'(\d+x\d+\s*cm)$', full_description)
                    if dimension_match:
                        product_data['dimensions'] = dimension_match.group(1).strip()
                        product_data['description'] = re.sub(r',\s*\d+x\d+\s*cm$', '', full_description).strip()
                    else:
                        product_data['dimensions'] = None
                        product_data['description'] = full_description
                
                    # --- Stage 2: Fetch the individual product page for category ---
                    if product_data['url']:
                        try:
                            print(f"  > Fetching details for: {product_data['name']}")
                            product_page_response = requests.get(product_data['url'], headers=headers, timeout=10)
                            product_page_response.raise_for_status()
                        
                            category_path = get_full_category_path(product_page_response.text)
                            product_data['category_path'] = " > ".join(category_path)
                        
                            time.sleep(0.5) # Delay between individual product requests

                        except requests.RequestException as e:
                            print(f"    ! Could not fetch product page {product_data['url']}: {e}")
                            product_data['category_path'] = 'Error fetching category'
                    else:
                        product_data['category_path'] = 'URL not found'

                    all_products.append(product_data)
            
                # Move to the next page
                current_page += 1
                time.sleep(1) # Delay between API page requests

            except requests.RequestException as e:
                print(f"Failed to fetch API page {current_page}: {e}")
                break
            except ValueError: # Catches JSON decoding errors
                print(f"Failed to decode JSON from API page {current_page}.")
                break

        print(f"\nScraping complete. Total products found: {len(all_products)}")
        return all_products

    # --- Main execution block ---
    if __name__ == '__main__':
        scraped_data = scrape_ikea_beds_api()

        if scraped_data:
            df = pd.DataFrame(scraped_data)
        
            print("\n--- Sample of Scraped Data ---")
            print(df.head())
        
            print(f"\nTotal items scraped: {len(df)}")

            try:
                df.to_csv('ikea_beds_data_api.csv', index=False, encoding='utf-8-sig')
                print("\nData successfully saved to ikea_beds_data_api.csv")
            except Exception as e:
                print(f"\nError saving data to CSV: {e}")
    return


if __name__ == "__main__":
    app.run()
