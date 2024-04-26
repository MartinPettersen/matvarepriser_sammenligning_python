
from api.get_api_data import get_products
from api.get_products_with_ean import get_products_with_ean
from database.data_access import create_database, insert_products


#json_object = json.dumps(products, indent=4)

#with open("products.json", "w") as file:
#   file.write(json_object)

products = get_products()
create_database()

# print(len(products["data"]))

#   merkevare, bilde (hvis tilgjengelig) og produkt-ID

products_with_same_ean = get_products_with_ean(7035620025037)

print(len(products_with_same_ean["data"]["products"]))


for product in products["data"]:

    if product["id"] == 32:
        print(product)

#    print(product["id"])
#    print(product["ean"])
#    print(product["name"])
#    print(product["description"])
#    print(product["category"]) 
#    print(product["brand"])
#    print(product["image"])

    

    # print(product["store"])
    insert_products(product["id"], product["ean"], product["name"],product["description"], product["category"], product["brand"], product["image"] )
    print("-------------------")

