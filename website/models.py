from . import *
from flask_login import UserMixin

class Product(db.Model):
    productId = db.Column(db.Integer, primary_key=True)
    productName = db.Column(db.String(50))
    desc = db.Column(db.String(250))
    cost = db.Column(db.Integer, primary_key=False)
    imagePath = db.Column(db.String(250))
    imageName = db.Column(db.String(250))
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    userName = db.Column(db.String(150))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    firstName = db.Column(db.String(150))
    products = db.relationship('Product')
    admin = db.Column(db.Boolean)   
    banned = db.Column(db.Boolean)
