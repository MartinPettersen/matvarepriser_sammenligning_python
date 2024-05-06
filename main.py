
from api.get_api_data import get_products
from api.get_products_with_ean import get_products_with_ean
from api.get_products_with_id import get_products_with_id
from api.get_price_data import get_price_data
from database.data_access import compare_stores, create_database, insert_products, fetch_products, fetch_prices
from flask import Flask, jsonify

from api.get_stores_close_by import get_stores_by_procimity

products = get_products()

try:
    create_database()
except:
    pass

print(f"number of products: {len(products['data'])}")
for product in products["data"]:

    #if product["id"] == 32:
        #print(product)

#    print(product["id"])
#    print(product["ean"])
#    print(product["name"])
#    print(product["description"])
#    print(product["category"]) 
#    print(product["brand"])
#    print(product["image"])


    # print(product["store"])
    insert_products(product["id"] or 'Mangler ID', product["ean"] or 'Mangler ean', product["name"] or 'Mangler navn',product["description"] or 'Mangler beskrivelse', product["category"] or 'Mangler Kategori', product["brand"] or 'Mangler merkevare', product["image"] or "https://bilder.ngdata.no/7035620025037/meny/large.jpg" )
    # print(get_price_data(product["ean"]))
    print("-----------------------")
    

print("The products:")
#produkter = fetch_products()
#temp_prices = fetch_prices(produkter[0][1])
#print(temp_prices)

#for product in produkter:
#    if product[1] != "Missing EAN":
#        
#        print(f"Product {product[2]} with EAN {product[1]} ")
#        print("Prices at stores from lowest to highest:")
#        product_prices = fetch_prices(product[1])
#        for product_price in product_prices:
#            print(f"Sold at {product_price[1]} for {product_price[2]}")
        

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'hello, world'


@app.route('/products', methods=['GET'])
def get_products():
    produkter = fetch_products()
    
    return produkter


@app.route('/product/price/<ean>', methods=['GET'])
def get_product_prices(ean):
    return fetch_prices(ean)


@app.route('/product/price/<ean>search_query=<query>', methods=['GET'])
def compare_store_prices(ean, query):
    print("i get called")
    
    return compare_stores(ean, query)

print(get_stores_by_procimity(59.00, 10.20))
if __name__ == '__main__':
    app.run()
    pass
