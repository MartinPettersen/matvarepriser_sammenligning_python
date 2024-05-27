import json


def price_comparison(price_list):
    
    #print(f"\n\n\nthe price_list in price comparison: {price_list}")
    rows = []
    placement = 1
    latest_price = price_list[0][2]
    cheapest = price_list[0][2]
    
    combined = 0
    
    for row in price_list:
        print(f"\n\npricelist row[3]: {row[3]}\n\n")
        
        if row[2] != latest_price:
            placement += 1
            latest_price = row[2]

        combined += row[2]        
        one_percent = cheapest / 100
        more_exspensive = round(((row[2] - cheapest) / one_percent),2)
        
        store_price = {
            "ean": row[0],
            "store" : row[1],
            "price" : row[2],
            "price_history": json.loads(row[3]),
            "created_at": row[4],
            "updated_at": row[5],
            "ranking": placement,
            "price_increase": more_exspensive,
        }
        rows.append(store_price)
        
    average = combined / len(rows)        
    
    store_list = {
        "store_prices": rows,
        "average": average,
        "mean": rows[round(len(rows) / 2)]["price"],
    }
    
    return store_list
