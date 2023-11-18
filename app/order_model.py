import enum
from .db import db

class OrderState(enum.Enum):
    Composing = "composing"
    Preparing = "preparing"
    Delivering = "delivering"
    Completed = "completed"

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('user_customer.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('user_restaurant.id'))
    delivery_id = db.Column(db.Integer, db.ForeignKey('user_delivery.id'))
    food_items = db.Column(db.String(1000))
    order_state = db.Column(db.Enum(OrderState))
    sum_total = db.Column(db.Integer)