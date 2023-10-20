import time
import requests
import json
from bs4 import BeautifulSoup

def getNikeProduct():

    with open('shoes.json', 'r') as file:
        brands_data = json.load(file)

    url = "https://www.nike.com/vn/w/walking-shoes-b3e0kzy7ok"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'Accept-Language': 'vi-VN,vi;q=0.9'
    }

    response = requests.get(url,headers=headers)

    if response.status_code==200:
        soup = BeautifulSoup(response.content,'html.parser')
        
        for item in soup.select('[id="skip-to-products"] .product-card__body'):

            name = item.select_one('[tabindex="-1"]').text
            url_product = item.select_one('[class*="product-card__link-overlay"]')['href']
            # print(name)
            # print(url_product)
            time.sleep(2)

            detailInfo = getDetailNikeProduct(url_product)
            
            if detailInfo:
                image_src = detailInfo.get('image_src', '')
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

            for brand_data in brands_data:
                if brand_data["brand"] == "Nike":
                    brand_data["products"].append(productInfo)
                    break

    else:
        print(f"Request failed with status code: {response.status_code}")

    with open('shoes.json', 'w') as file:
        json.dump(brands_data, file, indent=2)

def getDetailNikeProduct(url_product):
    try:
        headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'Accept-Language': 'vi-VN,vi;q=0.9'
        }

        response = requests.get(url_product,headers=headers)

        if response.status_code==200:

            soup = BeautifulSoup(response.content, 'html.parser')

            price = soup.select_one('[data-test="product-price"]').text
            
            image_src = soup.select_one('[data-fade-in="css-147n82m"]')['src']
            
            data_script = soup.select_one('[id="__NEXT_DATA__"]').text
            
            if data_script:
                detail_information=list()
                
                parsed_data = json.loads(data_script)
                print("----------------data_script loaded-----------------")

                product_key = list(parsed_data['props']['pageProps']['initialState']['Threads']['products'].keys())[0]
                
                raw_detail_information = parsed_data['props']['pageProps']['initialState']['Threads']['products'][product_key].get('description',{})

                description = parsed_data['props']['pageProps']['initialState']['Threads']['products'][product_key].get('descriptionPreview',{})

                html_detail_information = BeautifulSoup(raw_detail_information, 'html.parser')

                for detail in html_detail_information.select('[class*="headline-5"]'):
                    detail_text = detail.text
                    if detail_text=='\xa0' or detail_text.casefold()=='More Benefits'.casefold() or detail_text.casefold()=='Product details'.casefold():
                        continue
                    detail_information.append(detail_text)

                return {
                    "price": price,
                    "description": description,
                    "detail_information": detail_information,
                    "image_src": image_src
                }
            else:
                print("---------------data_script not found.--------------")
            
    except Exception as e:
        print(e)
    return None
getNikeProduct()