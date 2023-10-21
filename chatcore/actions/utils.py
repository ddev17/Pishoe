import json
import os
import random
import re

def parse_brand_from_question(question):
  brands = ["adidas", "nike", "puma"]
  brand_of_question = []
  for brand in brands:
    if re.search(f"\\b{brand}\\b", question.lower()):
      brand_of_question.append(brand.capitalize())
  return brand_of_question

def parse_size_from_question(question):
    pattern = r'(?:(?:size|sz)\s)(\d+)'
    size = re.findall(pattern, question.lower())
    if len(size) > 0:
        return size[0]
    return None

def parse_price_from_question(question):
    pattern = r'(\d+\s*(trieu|tram|chuc|k))'
    price_parse = []
    price_in_question = re.findall(pattern, question.lower())
    if len(price_in_question) > 0:
        for price_raw in price_in_question:
            price_str = price_raw[0]
            price_number = int(re.sub(r'[^0-9]', '', price_str))
            if 'trieu' in price_str:
                price_parse.append(price_number * 1000000)
            if 'tram' in price_str or 'cham' in price_str:
                price_parse.append(price_number * 100000)
            if 'chuc' in price_str or 'truc' in price_str:
                price_parse.append(price_number * 10000)
            if 'vnd' in price_str or 'dong' in price_str:
                price_parse.append(price_number)
            if 'k' in price_str:
                price_parse.append(price_number)
    return sorted(price_parse)

def no_accent_vietnamese(s):
    s = re.sub(r'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', s)
    s = re.sub(r'[ÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪ]', 'A', s)
    s = re.sub(r'[èéẹẻẽêềếệểễ]', 'e', s)
    s = re.sub(r'[ÈÉẸẺẼÊỀẾỆỂỄ]', 'E', s)
    s = re.sub(r'[òóọỏõôồốộổỗơờớợởỡ]', 'o', s)
    s = re.sub(r'[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]', 'O', s)
    s = re.sub(r'[ìíịỉĩ]', 'i', s)
    s = re.sub(r'[ÌÍỊỈĨ]', 'I', s)
    s = re.sub(r'[ùúụủũưừứựửữ]', 'u', s)
    s = re.sub(r'[ƯỪỨỰỬỮÙÚỤỦŨ]', 'U', s)
    s = re.sub(r'[ỳýỵỷỹ]', 'y', s)
    s = re.sub(r'[ỲÝỴỶỸ]', 'Y', s)
    s = re.sub(r'[Đ]', 'D', s)
    s = re.sub(r'[đ]', 'd', s)
    return s

def get_recommend_special_product(brands, price_range):
    core_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    shoes_data_path = os.path.join(core_dir, 'data', 'shoes.json')
    recommend_list = []
    with open(shoes_data_path, 'r') as file:
        shoes_data = json.load(file)

    brand = random.choice(brands)

    filtered_products = [product for brand_data in shoes_data if brand_data["brand"] == brand for product in
                         brand_data["products"]]

    if len(price_range) > 1:
        filtered_products = [product for product in filtered_products if
                             price_range[0] <= int(re.sub(r'[^0-9]', '', product["price"])) <= price_range[
                                 1]]

    recommend_list = []
    if filtered_products:
        recommend_product = random.choice(filtered_products)
        recommend_product["brand"] = brand
        recommend_list.append(recommend_product)
    else:
        print("No products match the given conditions.")
    return recommend_list

def get_recommend_product(count):
    core_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    shoes_data_path = os.path.join(core_dir, 'data', 'shoes.json')
    recommend_list = []
    with open(shoes_data_path, 'r') as file:
        shoes_data = json.load(file)

    for i in range(count):
        all_shoes_of_brand = random.choice(shoes_data)
        brand = all_shoes_of_brand["brand"]
        recommend_product = random.choice(all_shoes_of_brand["products"])
        recommend_product["brand"] = brand
        recommend_list.append(recommend_product)
    return recommend_list