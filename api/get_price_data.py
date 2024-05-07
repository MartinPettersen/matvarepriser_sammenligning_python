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

    products_with_same_ean = get_products_with_ean(ean)

    # print(len(products_with_same_ean["data"]["products"]))

    #print(products_with_same_ean["data"]["products"])
    #print("\n\n\n\n\n\n\n")
    #print(len(products_with_same_ean["data"]["products"]))

    if type(products_with_same_ean["data"]["products"]) != "NoneType":
        store_prices = [{"store": product["store"]["name"] or 'Mangler butikk', "current_price": product["current_price"] or 'Mangler pris' } for product in products_with_same_ean["data"]["products"]]
    else:
        store_prices = "no data"
    #for pr in products_with_same_ean["data"]["products"]:
    #    print(pr["name"])
    
    #    print(pr["current_price"])
    #    print(pr["store"]["name"])
    
    return store_prices
     