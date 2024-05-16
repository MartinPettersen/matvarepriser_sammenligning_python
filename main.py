
from api.get_api_data import get_products
from api.get_products_with_ean import get_products_with_ean
from api.get_products_with_id import get_products_with_id
from api.get_price_data import get_price_data
from database.data_access import check_for_key, compare_stores, create_database, create_user_table, fetch_product, fetch_user, fetch_userfavourites, insert_key, insert_products, fetch_products, fetch_prices, insert_user, insert_userfavourites
from flask import Flask, jsonify, request
from flask_cors import CORS
from uuid import uuid4

from api.get_stores_close_by import get_stores_by_procimity
from price_comparison import price_comparison

create_user_table()

try:
    products = get_products()

    create_database()

    for product in products["data"]:
        insert_products(product["id"] or 'Mangler ID', product["ean"] or 'Mangler ean', product["name"] or 'Mangler navn',product["description"] or 'Mangler beskrivelse', product["category"] or 'Mangler Kategori', product["brand"] or 'Mangler merkevare', product["image"] or "https://bilder.ngdata.no/7035620025037/meny/large.jpg" )
except:
    pass
    

     

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_new_user():
    new_key = str(uuid4())
    insert_key(new_key)
    return f'This is a simple API ment to be practice, your user key is: {new_key}'

@app.route('/product/<id>')
def get_product_by_id(id):
    product_data = fetch_product(id)
    #print(f"the product is {product_data}")
    product = {
                "id": product_data[0][0],
                "ean": product_data[0][1],
                "name": product_data[0][2],        
                "description": product_data[0][3],
                "category": product_data[0][4],
                "brand": product_data[0][5],
                "image": product_data[0][6],
                "created_at": product_data[0][7],        
                "updated_at": product_data[0][8],        
            }
    return product


@app.route('/api/favourite', methods=['POST'])
def insert_favourite_product():
    data = request.json
    user_id = data.get("user_id")
    product_ean = data.get("product_ean")
    insert_userfavourites(user_id, product_ean)

@app.route('/api/checkfavourite', methods=['POST'])
def check_if_favourite():
    data = request.json
    user_id = data.get("user_id")
    product_ean = data.get("product_ean")
    check_if_favourite(user_id, product_ean)

@app.route('/api/getfavourites', methods=['POST'])
def get_user_favourites():
    data = request.json
    user_id = data.get("user_id")
    fetch_userfavourites(user_id)

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
        the_price_list = fetch_prices(ean)
        
        price_list = price_comparison(the_price_list)
        
        return price_list
    else:
        return "Unathorized Access"



@app.route('/product/price/<ean>search_query=<query>', methods=['GET'])
def compare_store_prices(ean, query):
    user_key = request.headers.get('Authorization')
    test = check_for_key(user_key)
    print(query)
    
    stores = compare_stores(ean, query)
    
    store_list = price_comparison(stores)
    
    
    if test:
        return store_list
    else:
        return "Unathorized Access"
    
@app.route('/stores/proximity/lat=<lat>&lng=<lng>&km=<km>', methods=['GET'])
def get_stores_by_proximity(lat, lng, km):
    user_key = request.headers.get('Authorization')
    test = check_for_key(user_key)
    
    if test:
        return get_stores_by_procimity(lat, lng, km)
    else:
        return "Unathorized Access"


@app.route('/api/createuser', methods=['POST'])
def create_user():
    data = request.json
    password = data.get("password")
    email = data.get("email")
    name = data.get("name")
    id = data.get("id")
    
    print(f"i recieved {email} and {password}")

    insert_user(id, name, email, password)

    return jsonify({'message': f"you sent {email} and {password}"})


@app.route('/api/getuser', methods=['POST'])
def get_user():
    data = request.json
    email = data.get("email")
    print("trying to get user")
    print(f"the email {email}")
    user = fetch_user(email)
    print(user)
        
    user_data = {
        "id": user[0][0],
        "name": user[0][1],
        "email": user[0][2],
        "password": user[0][3],
        "created_at": user[0][4],
        "updated_at": user[0][5],
    }
    print(user_data)
    return jsonify({'user': user_data})


# http://127.0.0.1:5000/
# http://127.0.0.1:5000/products
# http://127.0.0.1:5000/product/price/7035620025037
# http://127.0.0.1:5000/product/price/7035620025037search_query=KIWI+Joker
# http://127.0.0.1:5000/stores/proximity/lat=63.4308&lng=10.4034



if __name__ == '__main__':
    app.run()
    #app.run(ssl_context='adhoc')
    pass
