import requests
import json
import os
from dotenv import load_dotenv

import pandas

NUMBER_OF_PRODUCTS = 100

load_dotenv()

def get_stores_by_procimity(lat, lng):
    print("lat long")
    try:
        url = f"https://kassal.app/api/v1/physical-stores?lat=59.9333&lng=10.7166"
        headers = { "Authorization": f"Bearer {os.getenv('KASSAL_KEY')}"}
        res = requests.get(url, headers=headers)
        print(res)
        return res.json()
    except requests.exceptions.RequestException as e:
        print(f"There has been an error: {e}")
        
