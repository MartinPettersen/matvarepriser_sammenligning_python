import sqlite3
import json

from api.get_price_data import get_price_data

connection = sqlite3.connect("matvarepriser.db",check_same_thread=False)

cursor = connection.cursor()

def create_database():

    cursor.execute("CREATE TABLE product(id, ean, name, description, category JSON, brand, image,created_at TEXT NOT NULL DEFAULT current_timestamp, TEXT NOT NULL DEFAULT current_timestamp)")
    cursor.execute("DROP TABLE IF EXISTS pricelist")
    cursor.execute("CREATE TABLE pricelist(ean, store, price, created_at TEXT NOT NULL DEFAULT current_timestamp, TEXT NOT NULL DEFAULT current_timestamp)")

def insert_products(id, ean, name, description, category, brand, image):
    
    cursor.execute("DROP TABLE IF EXISTS temp_category")
    cursor.execute("CREATE TEMP TABLE temp_category (id INT, depth INT, name TEXT)")

    categories = []
    category_list = []

    if category == 'Mangler Kategori':
        print(f"category is none the id is {id}")
    else:
        for cate in category:
            categories.append({'id': cate['id'], 'depth': cate['depth'], 'name': cate['name']})


        for cat in categories:
            cursor.execute('INSERT INTO temp_category (id, depth, name) values (?, ?, ?)',
                          (cat['id'], cat['depth'], cat['name']) )

    

        for row in cursor.execute('SELECT id, depth, name FROM temp_category'):
            category_dict = {'id': row[0], 'depth': row[1], 'name': row[2]}
            category_list.append(category_dict)

    category_json_array = json.dumps(category_list)

    
    cursor.execute(f"""INSERT INTO product VALUES (?, ?, ?, ?, json(?), ?, ?, current_timestamp, current_timestamp)""", (id, ean, name, description, category_json_array, brand, image) )
    
    res = cursor.execute("SELECT name FROM product")
    test = res.fetchall()
    print(test)
    test_time = cursor.execute("SELECT created_at FROM product")
    time = test_time.fetchall()
    print(time)
    print(f"is was created at {time}")
    

def fetch_products():
    res = cursor.execute("SELECT * FROM product")
    test = res.fetchall()
    return test

def fetch_prices(ean):
    insert_prices(ean)
    res = cursor.execute("SELECT * FROM pricelist WHERE ean = ? ORDER BY price ASC", (ean,))
    test = res.fetchall()
    return test    
        
def compare_stores(ean, query):
    insert_prices(ean)
    queries = query.split("+")
    test_que = [ "Meny","KIWI"]
    
    stores = ""
    for  i in range(0,len(test_que)):
        if i > 0:
            stores += f"OR store = ? "
        else:
            stores += f"AND store = ?  "
            
    print(stores)
    combined_list = []
    for store in queries:
        res = cursor.execute(f"SELECT * FROM pricelist WHERE ean = ? AND store = ?  ORDER BY price ASC", (ean, store))
        test = res.fetchall()
        print(test)
        print("rin in here")
        combined_list += test
        
    print(combined_list)
    print(queries)
    combined_list.sort(key=lambda x: x[1], reverse=False)    
    print(combined_list)
    
    return combined_list

def insert_prices(ean):

    try:
        store_prices = get_price_data(ean)
    
        cursor.execute("SELECT 1 FROM pricelist WHERE ean = ?", (ean,))
        exists = cursor.fetchone()
    
        if not exists:
            for store_price in store_prices:
                #print(store_price)
                #print(ean)
                # print(store_price["current_price"]["price"])
            
                #print(ean, store_price.store, store_prices.current_price)
                cursor.execute('INSERT INTO pricelist VALUES (?, ?, ?, current_timestamp, current_timestamp)',(ean, store_price["store"], store_price["current_price"]["price"]))
        else:
            print("Allready exists")
    except:
        print("Missing EAN")

    