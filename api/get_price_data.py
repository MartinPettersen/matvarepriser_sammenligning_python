import requests
import json
import os
from dotenv import load_dotenv

import pandas

NUMBER_OF_PRODUCTS = 100

load_dotenv()

def get_products_with_ean(ean):
    url = f"https://kassal.app/api/v1/products/ean/{ean}"
    headers = { "Authorization": f"Bearer {os.getenv('KASSAL_KEY')}"}
    res = requests.get(url, headers=headers)
    return res.json()


def get_price_data(ean):

    products_with_same_ean = get_products_with_ean(7035620025037)

    # print(len(products_with_same_ean["data"]["products"]))

    #print(products_with_same_ean["data"]["products"])

    store_prices = [{"store": product["store"]["name"], "current_price": product["current_price"] } for product in products_with_same_ean["data"]["products"]]

    #for pr in products_with_same_ean["data"]["products"]:
    #    print(pr["name"])
    
    #    print(pr["current_price"])
    #    print(pr["store"]["name"])
    
    return store_prices
     