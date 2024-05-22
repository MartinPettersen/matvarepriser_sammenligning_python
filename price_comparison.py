def price_comparison(price_list):
    rows = []
    placement = 1
    print("the pricelist in price_comparison")
    print(price_list)
    latest_price = price_list[0][2]
    cheapest = price_list[0][2]
    
    for row in price_list:
        
        if row[2] != latest_price:
            placement += 1
            latest_price = row[2]
        
        one_percent = cheapest / 100
        more_exspensive = round(((row[2] - cheapest) / one_percent),2)
        
        store_price = {
            "ean": row[0],
            "store" : row[1],
            "price" : row[2],
            "created_at": row[3],
            "updated_at": row[4],
            "ranking": placement,
            "price_increase": more_exspensive,
        }
        rows.append(store_price)
        
    store_list = {
        "store_prices": rows
    }
    
    return store_list
