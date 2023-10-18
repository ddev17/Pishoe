import time
import requests
import json
from bs4 import BeautifulSoup

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

            description = soup.select_one('[data-uds-child="text"]').text
            
            return {
                    "price": price,
                    "image_src": image_src,
                    "name": name,
                    "description": description
                }
    except Exception as e:
        print(e)
    return None

def getPumaProduct():

    with open('shoes.json', 'r') as file:
        brands_data = json.load(file)


    url = "https://us.puma.com/us/en/men/shop-all-mens?pref_productdivName=Shoes&offset=408"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    }

    response = requests.get(url,headers=headers)

    if response.status_code==200:
        soup = BeautifulSoup(response.content,'html.parser')

        for item in soup.select('[data-test-id="product-list-item"]'):
            url_product = item.select_one('[data-test-id="product-list-item-link"]')['href']

            time.sleep(3)

            detailInfo = getDetailPumaProduct(f"https://us.puma.com{url_product}")
            
            if detailInfo:
                image_src = detailInfo.get('image_src', '')
                description = detailInfo.get('description', '')
                detail_information = detailInfo.get('detail_information', '')
                price = detailInfo.get('price', '')
                name = detailInfo.get('name','')
            else:
                description = None
                price = None

            productInfo = {
                "image_src": image_src,
                "name": name,
                "source": url_product,
                "description": description,
                "detail_information": detail_information,
                "price": price,
            }
            print(productInfo)

            for brand_data in brands_data:
                if brand_data["brand"] == "Puma":
                    brand_data["products"].append(productInfo)
                    break
            
    else:
        print(f"Request failed with status code: {response.status_code}")

    with open('shoes.json', 'w') as file:
        json.dump(brands_data, file, indent=2)

getPumaProduct()
