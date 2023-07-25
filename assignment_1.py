import time
import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrapeProduct(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    products = []

    product_containers = soup.find_all('div', {'data-component-type': 's-search-result'})

    for container in product_containers:
        product_url = container.h2.a['href']
        product_url = f"https://www.amazon.in{product_url}"
        product_response = requests.get(product_url)
        product_soup = BeautifulSoup(product_response.content, 'html.parser')

        product_name = container.h2.a.span.text.strip()

        price_tag = container.find('span', {'class': 'a-offscreen'})
        product_price = price_tag.text.strip() if price_tag else 'Not available'

        rating_tag = container.find('span', {'class': 'a-icon-alt'})
        product_rating = rating_tag.text.strip() if rating_tag else 'Not available'

        description_tag = product_soup.find('meta', {'name': 'description'})
        product_description = description_tag.get('content').strip() if description_tag else 'Not available'

        asin_tag = product_soup.find('span', {'class': 'product-asin'})
        product_asin = asin_tag.text.strip() if asin_tag else 'Not available'

        manufacturer_tag = product_soup.find('a', {'id': 'bylineInfo'})
        product_manufacturer = manufacturer_tag.text.strip() if manufacturer_tag else 'Not available'

        products.append({
            'Product Name': product_name,
            'Price': product_price,
            'Rating': product_rating,
            'URL': product_url,
            'Description': product_description,
            'ASIN': product_asin,
            'Manufacturer': product_manufacturer
        })

        time.sleep(2)
        
    return products

def scrapePages(url, np):
    all_products = []
    for page_num in range(1, np + 1):
        url = f"{url}&page={page_num}"
        products = scrapeProduct(url)
        all_products.extend(products)
    return all_products

url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"
np = 20
data = scrapePages(url, np)
df = pd.DataFrame(data)
df.to_csv('data.csv', index=True)