import sqlite3
import json

connection = sqlite3.connect("matvarepriser.db")

cursor = connection.cursor()

def create_database():
    print("i run")

    cursor.execute("CREATE TABLE product(id, ean, name, description, category JSON, brand, image)")


def insert_products(id, ean, name, description, category, brand, image):
    
    cursor.execute("DROP TABLE IF EXISTS temp_category")
    cursor.execute("CREATE TEMP TABLE temp_category (id INT, depth INT, name TEXT)")

    categories = []

    if category is None:
        print(f"category is none the id is {id}")

    for cate in category:
        categories.append({'id': cate['id'], 'depth': cate['depth'], 'name': cate['name']})


    for cat in categories:
        cursor.execute('INSERT INTO temp_category (id, depth, name) values (?, ?, ?)',
                      (cat['id'], cat['depth'], cat['name']) )

    
    category_list = []

    for row in cursor.execute('SELECT id, depth, name FROM temp_category'):
        category_dict = {'id': row[0], 'depth': row[1], 'name': row[2]}
        category_list.append(category_dict)

    category_json_array = json.dumps(category_list)

    
    cursor.execute(f"""INSERT INTO product VALUES (?, ?, ?, ?, json(?), ?, ?)""", (id, ean, name, description, category_json_array, brand, image) )
    
    
    #res = cursor.execute("SELECT image FROM product")
    #test = res.fetchall()
    #print(test)