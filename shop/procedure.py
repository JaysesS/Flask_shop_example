from operator import itemgetter

def query_view_product(query_result):
    products = [
        {
            'id' : x.id,
            'name' : x.name,
            'category' : x.category,
            'description' : x.description,
            'count' : x.count,
            'price' : x.price
        }
        for x in query_result
    ]
    return sorted(products, key=itemgetter('price'), reverse=True)
