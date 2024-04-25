import requests
import json
import os
from dotenv import load_dotenv

import pandas


load_dotenv()

def get_products():
    url = "https://kassal.app/api/v1/products?size=100"
    headers = { "Authorization": f"Bearer {os.getenv('KASSAL_KEY')}"}
    res = requests.get(url, headers=headers)
    return res.json()

products = get_products()

# json_object = json.dumps(products, indent=4)

# with open("products.json", "w") as file:
#    file.write(json_object)

print(len(products["data"]))