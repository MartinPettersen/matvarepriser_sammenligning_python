
from api.get_api_data import get_products
from api.get_products_with_ean import get_products_with_ean
from api.get_products_with_id import get_products_with_id
from api.get_price_data import get_price_data
from database.data_access import check_for_key, compare_stores, create_database, insert_key, insert_products, fetch_products, fetch_prices
from flask import Flask, jsonify, request
from uuid import uuid4

from api.get_stores_close_by import get_stores_by_procimity

products = get_products()

try:
    create_database()
except:
    pass

print(f"number of products: {len(products['data'])}")
for product in products["data"]:

    insert_products(product["id"] or 'Mangler ID', product["ean"] or 'Mangler ean', product["name"] or 'Mangler navn',product["description"] or 'Mangler beskrivelse', product["category"] or 'Mangler Kategori', product["brand"] or 'Mangler merkevare', product["image"] or "https://bilder.ngdata.no/7035620025037/meny/large.jpg" )
    

print("The products:")
     

app = Flask(__name__)

@app.route('/')
def hello_world():
    user_key = request.headers.get('Authorization')
    new_key = str(uuid4())
    print(new_key)
    insert_key(new_key)
    test = check_for_key(new_key)
    print(test)
    return f'This is a simple API ment to be practice {user_key}, your new key is: {new_key}'


@app.route('/products', methods=['GET'])
def get_products():
    user_key = request.headers.get('Authorization')
    print(user_key)
    test = check_for_key(user_key)
    print(test)
    
    if test:
        produkter = fetch_products()
    
        return produkter
    else:
        return "Unathorized Access"

@app.route('/product/price/<ean>', methods=['GET'])
def get_product_prices(ean):
    return fetch_prices(ean)


@app.route('/product/price/<ean>search_query=<query>', methods=['GET'])
def compare_store_prices(ean, query):
    print("i get called")
    
    return compare_stores(ean, query)

@app.route('/stores/proximity/lat=<lat>&lng=<lng>', methods=['GET'])
def get_stores_by_proximity(lat, lng):
    return get_stores_by_procimity(lat, lng)
    #lat=59.9333&lng=10.7166


print(get_stores_by_procimity(59.00, 10.20))
if __name__ == '__main__':
    app.run()
    pass
