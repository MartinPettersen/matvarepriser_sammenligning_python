def price_comparison(price_list):
    rows = []
    for row in price_list:
        store_price = {
            "ean": row[0],
            "store" : row[1],
            "price" : row[2],
            "created_at": row[3],
            "updated_at": row[4],
        }
        rows.append(store_price)
        
    store_list = {
        "store_prices": rows
    }
    
    return store_list
