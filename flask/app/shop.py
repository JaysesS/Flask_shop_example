from operator import itemgetter
from .models import Product, User
from app import db
import json, os

def view_products(filter = 'price'):
    pq = Product.query.all()
    products = [
        {
            'id' : x.id,
            'name' : x.name,
            'category' : x.category,
            'description' : x.description,
            'count' : x.count,
            'price' : x.price,
            'image' : x.image
        }
        for x in pq
    ]
    if len(filter.split(' ')) > 1:
        if filter.split(' ')[1] == 'min':
            filter = filter.split(' ')[0]
            return sorted(products, key=itemgetter(filter), reverse=False)
        elif filter.split(' ')[1] == 'max':
            filter = filter.split(' ')[0]
            return sorted(products, key=itemgetter(filter), reverse=True)
    return sorted(products, key=itemgetter(filter), reverse=True)

def remove_product_cart(cart, id):
    for i in range(len(cart)):
        if cart[i]['id'] == id:
            break
    del cart[i]
    return cart

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
        cost += item['price'] * item['amount']
    return cost

def get_money_by_username(username):
    user = User.query.filter_by(username = username).first()
    return user.money

def check_order(order, cart, user_wallet):
    if user_wallet < get_cost_cart(cart):
        return 'Need more money!'
    result = ""
    for item in order:
        product = get_product_dict(item["id"])
        if int(item["amount"]) > product['count']:
            result += f" We only have {product['count']} {product['name']}\n"
    return result

def update_cost_cart(cart, amount, id):
    for i in range(len(cart)):
        if cart[i]['id'] == id:
            cart[i]['amount'] = amount 
    return cart

def delete_all_products():
    Product.query.delete()
    db.session.commit()

def fill_all_products():
    filename = os.path.join(os.path.dirname(os.path.abspath(__file__)),"products.json")
    with open(filename, "r") as file:
        products = json.load(file)['products']
        for item in products:
            product = Product(
                name = item['name'],
                category = item['category'],
                description = item['description'],
                count = item['count'],
                price = item['price'],
                image = item['image'])
            db.session.add(product)
            db.session.commit()