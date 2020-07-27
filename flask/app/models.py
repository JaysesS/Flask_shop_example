from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique = True)
    password = db.Column(db.String(30))
    email = db.Column(db.String(60), unique = True)
    adress = db.Column(db.String(100))
    phone = db.Column(db.String(12))
    money = db.Column(db.Integer, default = 0)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    category = db.Column(db.String(20))
    description = db.Column(db.String(100))
    count = db.Column(db.Integer)
    price = db.Column(db.Integer)
    image = db.Column(db.String(100))

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    email= db.Column(db.String(60))
    adress = db.Column(db.String(100))
    phone = db.Column(db.String(12))
    product = db.Column(db.String(40))
    category = db.Column(db.String(40))
    count = db.Column(db.Integer)