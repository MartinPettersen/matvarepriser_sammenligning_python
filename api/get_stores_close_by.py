import requests
import json
import os
from dotenv import load_dotenv

import pandas

NUMBER_OF_PRODUCTS = 100

load_dotenv()

def get_stores_by_procimity(lat, lng, km):
    try:
        url = f"https://kassal.app/api/v1/physical-stores?lat={lat}&lng={lng}&km={km}"
        headers = { "Authorization": f"Bearer {os.getenv('KASSAL_KEY')}"}
        res = requests.get(url, headers=headers)
        return res.json()
    except requests.exceptions.RequestException as e:
        print(f"There has been an error: {e}")
        
