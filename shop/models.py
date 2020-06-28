from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique = True)
    password = db.Column(db.String(30))
    email = db.Column(db.String(60), unique = True)