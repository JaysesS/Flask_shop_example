from operator import itemgetter
from models import Product, User

def view_products():
    pq = Product.query.all()
    products = [
        {
            'id' : x.id,
            'name' : x.name,
            'category' : x.category,
            'description' : x.description,
            'count' : x.count,
            'price' : x.price
        }
        for x in pq
    ]
    return sorted(products, key=itemgetter('price'), reverse=True)

def get_product_dict(id):
    query_product = Product.query.filter_by(id = id).first()
    return {
            'id' : query_product.id,
            'name' : query_product.name,
            'category' : query_product.category,
            'description' : query_product.description,
            'count' : query_product.count,
            'price' : query_product.price
        }

def check_exist_product(cart, id):
    for item in cart:
        if item['id'] == id:
            return True
    return False

def update_amount_product(cart, id, amount):
    for i in range(len(cart)):
        if cart[i]['id'] == id:
            current_amount = cart[i]['amount']
            cart[i]['amount'] = current_amount + amount
    return cart

def get_cost_cart(cart):
    cost = 0
    for item in cart:
        cost += item['price']
    return cost

def get_money_by_username(username):
    user = User.query.filter_by(username = username).first()
    return user.money