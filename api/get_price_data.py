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

    print(f"get_price_data({ean})")
    products_with_same_ean = get_products_with_ean(ean)
    print("products with the sane ean")
    print(products_with_same_ean)
    try:    
        store_prices = []

        for product in products_with_same_ean["data"]["products"]:
            print(1)
            print("product in products with same ean")
            print(product)
            if product["store"] is not None and product["store"]["name"] is not None:
                store =  product["store"]["name"]
            else:
                store = 'Mangler butikk'
            print(2)
            print(f"the store is {store}")
            if product["current_price"] is not None:
                current_price =  product["current_price"]
            else:
                current_price = 'Mangler pris'
            print(f"the price is {current_price}")
            print(3)
            print("store prices before append")
            print(store_prices)
            store_prices.append({ "store": store, "current_price": current_price })
            print("store prices after append")           
            print(store_prices)
            
            print(4)
            print("-----------------------------------")
            print(store_prices)
            print("-----------------------------------")
            
    except:
        store_prices = []
    
    print("f")
    print(store_prices)
    return store_prices
     