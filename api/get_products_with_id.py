import requests
import json
import os
from dotenv import load_dotenv

import pandas

NUMBER_OF_PRODUCTS = 100

load_dotenv()

def get_products_with_id(id):
    url = f"https://kassal.app/api/v1/products/id/{id}"
    headers = { "Authorization": f"Bearer {os.getenv('KASSAL_KEY')}"}
    res = requests.get(url, headers=headers)
    return res.json()

