import json
import os
import random
import re

def parse_brand_from_question(question):
  brands = ["adidas", "nike", "puma"]
  brand_of_question = []
  for brand in brands:
    if re.search(f"\\b{brand}\\b", question.lower()):
      brand_of_question.append(brand)
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
            price_number = int(re.findall(r'\d+', price_str)[0])
            if 'trieu' in price_str:
                price_parse.append(price_number * 1000)
            if 'tram' in price_str or 'cham' in price_str:
                price_parse.append(price_number * 100)
            if 'chuc' in price_str or 'truc' in price_str:
                price_parse.append(price_number * 10)
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

def get_recommend_product(count):
    core_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    shoes_data_path = os.path.join(core_dir, 'data', 'shoes.json')
    shoes_data = None
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