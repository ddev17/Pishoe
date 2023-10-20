import json
import re

with open('shoes.json','r') as x:
    data = json.load(x)

for brand_data in data:
    #Navigate to Puma brand
    if brand_data["brand"] == "Nike":
        for i in range(len(brand_data["products"])):
            #Get USD price string
            price_raw = brand_data["products"][i]['price']
            #Get price string without $ sign
            res = price_raw.replace('Discounted from','')

            brand_data["products"][i]['price'] = res
#Save change to json
with open('shoes.json', 'w') as x:
    json.dump(data, x, indent=2)