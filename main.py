
from api.get_api_data import get_products
from api.get_products_with_ean import get_products_with_ean
from api.get_products_with_id import get_products_with_id
from api.get_price_data import get_price_data
from database.data_access import check_for_key, compare_stores, create_database, insert_key, insert_products, fetch_products, fetch_prices
from flask import Flask, jsonify, request
from flask_cors import CORS
from uuid import uuid4

from api.get_stores_close_by import get_stores_by_procimity

products = get_products()

try:
    create_database()
except:
    pass

for product in products["data"]:
    pass
    insert_products(product["id"] or 'Mangler ID', product["ean"] or 'Mangler ean', product["name"] or 'Mangler navn',product["description"] or 'Mangler beskrivelse', product["category"] or 'Mangler Kategori', product["brand"] or 'Mangler merkevare', product["image"] or "https://bilder.ngdata.no/7035620025037/meny/large.jpg" )
    

     

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_new_user():
    new_key = str(uuid4())
    insert_key(new_key)
    return f'This is a simple API ment to be practice, your user key is: {new_key}'


@app.route('/products', methods=['GET'])
def get_products():
    user_key = request.headers.get('Authorization')
    test = check_for_key(user_key)
    
    if test:
        produkter = fetch_products()    
        # print(produkter)
        
        rows = []
    
        for row in produkter:
            product = {
                "id": row[0],
                "ean": row[1],
                "name": row[2],        
                "description": row[3],
                "category": row[4],
                "brand": row[5],
                "image": row[6],
                "created_at": row[7],        
                "updated_at": row[8],        
            }
            rows.append(product)

        products = {
            "products": rows
        }
        
        return products
    else:
        return "Unathorized Access"

@app.route('/product/price/<ean>', methods=['GET'])
def get_product_prices(ean):
    user_key = request.headers.get('Authorization')
    test = check_for_key(user_key)
    
    if test:
        return fetch_prices(ean)
    else:
        return "Unathorized Access"

@app.route('/product/price/<ean>search_query=<query>', methods=['GET'])
def compare_store_prices(ean, query):
    user_key = request.headers.get('Authorization')
    test = check_for_key(user_key)
    
    if test:
        return compare_stores(ean, query)
    else:
        return "Unathorized Access"
    
@app.route('/stores/proximity/lat=<lat>&lng=<lng>', methods=['GET'])
def get_stores_by_proximity(lat, lng):
    user_key = request.headers.get('Authorization')
    test = check_for_key(user_key)
    
    if test:
        return get_stores_by_procimity(lat, lng)
    else:
        return "Unathorized Access"
    #lat=59.9333&lng=10.7166

# http://127.0.0.1:5000/
# http://127.0.0.1:5000/products
# http://127.0.0.1:5000/product/price/7035620025037
# http://127.0.0.1:5000/product/price/7035620025037search_query=KIWI+Joker
# http://127.0.0.1:5000/stores/proximity/lat=63.4308&lng=10.4034

if __name__ == '__main__':
    app.run()
    pass
