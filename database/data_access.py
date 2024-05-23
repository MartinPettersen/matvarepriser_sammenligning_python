import sqlite3
import json
from datetime import datetime

from api.get_price_data import get_price_data
from utils.compress import compress_text

connection = sqlite3.connect("matvarepriser.db",check_same_thread=False)

cursor = connection.cursor()

def create_database():

    cursor.execute("CREATE TABLE product(id, ean, name, description BLOB, category BLOB, brand, image,created_at TEXT NOT NULL DEFAULT current_timestamp,updated_at TEXT NOT NULL DEFAULT current_timestamp)")
    cursor.execute("CREATE TABLE product2(id, ean, name, description BLOB, category JSON, brand, image BLOB,created_at TEXT NOT NULL DEFAULT current_timestamp,updated_at TEXT NOT NULL DEFAULT current_timestamp)")
    
    cursor.execute("DROP TABLE IF EXISTS pricelist")
    cursor.execute("DROP TABLE IF EXISTS userfavourites")
    cursor.execute("CREATE TABLE pricelist(ean, store, price, created_at TEXT NOT NULL DEFAULT current_timestamp,updated_at TEXT NOT NULL DEFAULT current_timestamp)")
    cursor.execute("CREATE TABLE keyslist(key, created_at TEXT NOT NULL DEFAULT current_timestamp,updated_at TEXT NOT NULL DEFAULT current_timestamp)")
    cursor.execute("CREATE TABLE userdata(id type UNIQUE, name, email type UNIQUE, password, created_at TEXT NOT NULL DEFAULT current_timestamp,updated_at TEXT NOT NULL DEFAULT current_timestamp)")
    cursor.execute("CREATE TABLE userfavourites(user_id, product_id, created_at TEXT NOT NULL DEFAULT current_timestamp,updated_at TEXT NOT NULL DEFAULT current_timestamp)")

def insert_products(id, ean, name, description, category, brand, image):
    
    compressed_description = compress_text(description)
    
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
    compressed_category = compress_text(category_json_array)
    print("text version")
    print(category_json_array)
    print("compressed version")
    print(compressed_category)
    
    cursor.execute(f"""INSERT INTO product VALUES (?, ?, ?, ?, ?, ?, ?, current_timestamp, current_timestamp)""", (id, ean, name, compressed_description, compressed_category, brand, image) )
    connection.commit()


def create_user_table():
    #cursor.execute("DROP TABLE IF EXISTS userdata")
    #cursor.execute("CREATE TABLE userdata(id type UNIQUE, name, email type UNIQUE, password, created_at TEXT NOT NULL DEFAULT current_timestamp, TEXT NOT NULL DEFAULT current_timestamp)")
    cursor.execute("DROP TABLE IF EXISTS pricelist")
    cursor.execute("CREATE TABLE pricelist(ean, store, price, created_at TEXT NOT NULL DEFAULT current_timestamp,updated_at TEXT NOT NULL DEFAULT current_timestamp)")
    
    cursor.execute("DROP TABLE IF EXISTS userfavourites")
    
    cursor.execute("CREATE TABLE userfavourites(user_id, product_id, created_at TEXT NOT NULL DEFAULT current_timestamp, updated_at TEXT NOT NULL DEFAULT current_timestamp)")
  
def insert_user(id, name, email, password):
    try:
        cursor.execute('INSERT INTO userdata VALUES (?,?,?,?, current_timestamp, current_timestamp)',(id, name, email, password,))
        connection.commit()

    except sqlite3.DatabaseError as e:
        print(f"Database error: {e}")
        
    res = cursor.execute("SELECT * FROM userdata WHERE email = ?", (email,))
    test = res.fetchall()

def fetch_user(email):
    res = cursor.execute("SELECT * FROM userdata WHERE email = ?", (email,))
    test = res.fetchall()
    return test

def insert_userfavourites(id, product_id):
    try:
        cursor.execute('INSERT INTO userfavourites VALUES (?,?, current_timestamp, current_timestamp)',(id, product_id,))
        connection.commit()

    except sqlite3.DatabaseError as e:
        print(f"Database error: {e}")
        
    res = cursor.execute("SELECT * FROM userfavourites WHERE user_id = ?", (id,))
    test = res.fetchall()
    return check_for_favourite(id, product_id)

def delete_userfavourites(id, product_id):
    try:
        cursor.execute('DELETE FROM userfavourites WHERE user_id = ? AND product_id = ?',(id, product_id,))
        connection.commit()
        return "deleted"

    except sqlite3.DatabaseError as e:
        print(f"Database error: {e}")
        
def fetch_userfavourites(id):
    res = cursor.execute("SELECT * FROM userfavourites WHERE user_id = ?", (id,))
    test = res.fetchall()
    return test

def check_for_favourite(id, product_id):
    res = cursor.execute("SELECT * FROM userfavourites WHERE user_id = ? AND product_id = ?", (id, product_id,))
    test = res.fetchall()
    return len(test) != 0

def fetch_products():
    res = cursor.execute("SELECT * FROM product")
    test = res.fetchall()


    return test

def fetch_product(id):
    res = cursor.execute("SELECT * FROM product WHERE id = ?", (int(id),))
    test = res.fetchall()
    return test

def fetch_prices(ean):
    insert_prices(ean)
    try:
        res = cursor.execute("SELECT * FROM pricelist WHERE ean = ? ORDER BY price ASC", (ean,))
        test = res.fetchall()
        return test
    except:     
        return "Could not fetch prices"    
        
def compare_stores(ean, query):
    queries = query.split("+")
    stores = ""
    for  i in range(0,len(queries)):
        if i > 0:
            stores += f"OR store = ? "
        else:
            stores += f"AND store = ?  "
            
    combined_list = []
    
    
    for store in queries:
        res = cursor.execute(f"SELECT * FROM pricelist WHERE ean = ? AND store = ?  ORDER BY price ASC", (ean, store))
        test = res.fetchall()
        combined_list += test
        
    return combined_list

def insert_prices(ean):
    try:
    
        cursor.execute("SELECT 1 FROM pricelist WHERE ean = ?", (ean,))
        exists = cursor.fetchone()
    
        if not exists:
            store_prices = get_price_data(ean)
            if store_prices != "no data":
                json_object = json.dumps(store_prices, indent=4)
                with open("sample.json", "w") as outfile:
                    outfile.write(json_object)
                for store_price in store_prices:

                    cursor.execute('INSERT INTO pricelist VALUES (?, ?, ?, current_timestamp, current_timestamp)',(ean, store_price["store"], store_price["current_price"]["price"]))
                    connection.commit()
                
        else:
            
            res = cursor.execute("SELECT * FROM pricelist ORDER BY created_at DESC")
            test = res.fetchall()
            current_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            
            time_gap = (datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S') - datetime.strptime(test[0][4], '%Y-%m-%d %H:%M:%S')).seconds
            if time_gap > 70:
                store_prices = get_price_data(ean)
                
                for store_price in store_prices:
                    try:
                        cursor.execute('UPDATE pricelist SET store = ?,  price = ?, updated_at = ?  WHERE ean = ? AND store = ?',(store_price["store"], store_price["current_price"]["price"],  datetime.now().strftime('%Y-%m-%d %H:%M:%S'), ean, store_price["store"]))
                        connection.commit()
                    except Exception as e:
                        print("An error occurred:", e)    
                #res = cursor.execute("DELETE FROM pricelist where ean = ? ", (ean,))
                #insert_prices(ean)
            else:
                print("data is current")
    except sqlite3.DatabaseError as e:
        print(f"Database error: {e}")

    
    

def insert_key(user_key):
    
    ko
    
    try:
        cursor.execute('INSERT INTO keyslist VALUES (?, current_timestamp, current_timestamp)',(user_key,))
        connection.commit()

    except sqlite3.DatabaseError as e:
        print(f"Database error: {e}")

def check_for_key(user_key):
    res = cursor.execute("SELECT key FROM keyslist WHERE key = ?", (user_key,))
    test = res.fetchall()
    return len(test) != 0    
