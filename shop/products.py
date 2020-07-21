from models import Product
from app import db
import json

def delete_all_products():
    Product.query.delete()
    db.session.commit()

def fill_all_products():
    with open("products.json", "r") as file:
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