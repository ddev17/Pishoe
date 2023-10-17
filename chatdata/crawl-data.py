import time
import requests
import json
from bs4 import BeautifulSoup

# Function get name, url product adidas
def getAdidasProduct():
    # Open file data shoes.json
    with open('shoes.json', 'r') as file:
        brands_data = json.load(file)

    # Url adidas shoes page
    url = "https://www.adidas.com.vn/vi/nam-quan_vot-giay"

    payload = {}
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Sec-Fetch-Site': 'none',
        'Accept-Encoding': 'gzip, deflate, br',
        'Sec-Fetch-Mode': 'navigate',
        'Host': 'www.adidas.com.vn',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
        'Accept-Language': 'en-US,en;q=0.9',
        'Sec-Fetch-Dest': 'document',
        'Connection': 'keep-alive',
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.status_code == 200:
        # Request success, parse response
        soup = BeautifulSoup(response.content, 'html.parser')

        # Select elements using BeautifulSoup and iterate over them
        for item in soup.select('[data-auto-id="product_container"] .grid-item'):
            image_src = item.find('img')['src']
            name = item.select_one('.glass-product-card__title').text
            url_product = item.select_one('[class*="product-card-content-badges-wrapper"]')['href']
            print(image_src)
            # Sleep 5 second to stabilize request
            time.sleep(3)
            # Get detail product info
            detailInfo = getDetailAdidasProduct(f"https://www.adidas.com.vn{url_product}")

            if detailInfo:
                description = detailInfo.get('description', '')
                detail_information = detailInfo.get('detail_information', '')
                price = detailInfo.get('price', '')
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

            # Append data product to json
            for brand_data in brands_data:
                if brand_data["brand"] == "Adidas":
                    brand_data["products"].append(productInfo)
                    break
    else:
        print(f"Request failed with status code: {response.status_code}")

    # Save shoes data
    with open('shoes.json', 'w') as file:
        json.dump(brands_data, file, indent=2)

# Get detail adidas product info
def getDetailAdidasProduct(url_product):
    try:
        payload = {}
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Sec-Fetch-Site': 'none',
            'Accept-Encoding': 'gzip, deflate, br',
            'Sec-Fetch-Mode': 'navigate',
            'Host': 'www.adidas.com.vn',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
            'Accept-Language': 'en-US,en;q=0.9',
            'Sec-Fetch-Dest': 'document',
            'Connection': 'keep-alive',
        }

        response = requests.request("GET", url_product, headers=headers, data=payload)

        if response.status_code == 200:
            # Parse response
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract price
            price = soup.select_one('.gl-price-item').text.strip()

            data_script = None
            scripts = soup.find_all('script')
            for script in scripts:
                if 'window.DATA_STORE' in script.text:
                    data_script = script.text
                    break

            if data_script:
                parsed_data = json.loads(json.loads(data_script.replace('window.DATA_STORE = JSON.parse(', '').replace(');', '')))
                product_key = list(parsed_data['productStore']['products'].keys())[0]
                description = parsed_data['productStore']['products'][product_key]['data']['product_description'].get('text', {})
                detail_information = parsed_data['productStore']['products'][product_key]['data']['product_description'].get('usps', {})
                return {
                    "price": price,
                    "description": description,
                    "detail_information": detail_information
                }
            else:
                print("Script containing 'window.DATA_STORE' not found.")
        else:
            print(f"Request failed with status code: {response.status_code}")
    except Exception as e:
        print(e)
    return None

getAdidasProduct()