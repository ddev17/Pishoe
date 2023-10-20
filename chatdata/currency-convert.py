import json
import re

with open('shoes.json','r') as x:
    data = json.load(x)

for brand_data in data:
    #Navigate to Puma brand
    if brand_data["brand"] == "Puma":
        for i in range(len(brand_data["products"])):
            #Get USD price string
            price_raw = brand_data["products"][i]['price']
            #Get price string without $ sign
            res = re.findall(r'\d+', price_raw)
            #Convert to VND
            amount = int(res[0])*24500
            #Format result
            result = '{:,}'.format(amount)

            result+='\u20ab'

            brand_data["products"][i]['price'] = result
#Save change to json
with open('shoes.json', 'w') as x:
    json.dump(data, x, indent=2)