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
    try:    
        store_prices = []

        for product in products_with_same_ean["data"]["products"]:
            if product["store"] is not None and product["store"]["name"] is not None:
                store =  product["store"]["name"]
            else:
                store = None
            if product["current_price"] is not None:
                current_price =  product["current_price"]
            else:
                current_price = None
            if product["price_history"] is not None:
                price_history =  product["price_history"]
            else:
                price_history = None
            store_prices.append({ "store": store, "current_price": current_price, "price_history": price_history})        
            
    except:
        store_prices = []
    
    return store_prices
     