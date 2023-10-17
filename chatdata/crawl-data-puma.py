import time
import requests
import json
from bs4 import BeautifulSoup

def getPumaProduct():

    url = "https://us.puma.com/us/en/men/shop-all-mens?pref_productdivName=Shoes&offset=24"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    }

    response = requests.get(url,headers=headers)

    if response.status_code==200:
        soup = BeautifulSoup(response.content,'html.parser')

        for item in soup.select('[data-test-id="product-list-item"]'):
            url_product = item.select_one('[data-test-id="product-list-item-link"]')['href']

            detailInfo = getDetailPumaProduct(f"https://us.puma.com{url_product}")
            break
            
    else:
        print(f"Request failed with status code: {response.status_code}")

def getDetailPumaProduct(url_product):
    try:
        headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        }

        response = requests.get(url_product,headers=headers)

        if response.status_code==200:

            soup = BeautifulSoup(response.content, 'html.parser')

            name = soup.select_one('[data-uds-child="heading"]').text

            price = soup.select_one('[data-test-id="item-price-pdp"]').text

            image_src = soup.select_one('[data-test-id="pdp-main-image"]')['src']

            # description_outer = soup.select_one('[data-uds-child="text"]')

            # description = description_outer.select_one('p').text

            product_info_html = soup.select_one("#product-story li")

            # product_section = product_info_html.select_one('ul')

            print(product_info_html)
    except Exception as e:
        print(e)
    return None

# getPumaProduct()

getDetailPumaProduct('https://us.puma.com/us/en/pd/puma-x-lamelo-ball-mb-03-lafranc%C3%A9-mens-basketball-shoes/379233?swatch=01&referrer-category=mens-shop-all-mens')