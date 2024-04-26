
from api.get_api_data import get_products
from api.get_products_with_ean import get_products_with_ean
from api.get_products_with_id import get_products_with_id
from api.get_price_data import get_price_data
from database.data_access import create_database, insert_products


#json_object = json.dumps(products, indent=4)

#with open("products.json", "w") as file:
#   file.write(json_object)

products = get_products()
create_database()

# print(len(products["data"]))

#   merkevare, bilde (hvis tilgjengelig) og produkt-ID



#products_with_same_ean = get_products_with_ean(7035620025037)

#print(len(products_with_same_ean["data"]["products"]))

##print(products_with_same_ean["data"]["products"])

#for pr in products_with_same_ean["data"]["products"]:
#    print(pr["name"])
#    
#    print(pr["current_price"])
#    print(pr["store"]["name"])
#    
#    print("-----------------------")
#    print(f"elenfant: {None or 'dead'}")




#products_with_same_id = get_products_with_id(1)

#print(len(products_with_same_id["data"]))
#print(products_with_same_id["data"]["vendor"])

#print(products_with_same_ean["data"]["products"])

#for pr in products_with_same_id["data"]:
#    print(pr)







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
    

