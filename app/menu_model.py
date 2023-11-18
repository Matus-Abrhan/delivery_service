from .db import db

class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # username = db.Column(db.String(100), unique=True, nullable=False)
    # password = db.Column(db.String(100), nullable=False)
    # wallet = db.Column(db.Integer)
    # user_type = db.Column(db.Enum(UserEnum))
    restaurant_id =  db.Column(db.Integer, db.ForeignKey('user_restaurant.id'))
    food_items = db.relationship("FoodItem")

class FoodItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'))
    category = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)

