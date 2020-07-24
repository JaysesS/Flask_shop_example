from .models import Product
from app import db
import json, os

def delete_all_products():
    Product.query.delete()
    db.session.commit()

def fill_all_products():
    if os.path.isfile("products.json"):
        filename = "products.json"
    else:
        filename = "app/products.json"
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