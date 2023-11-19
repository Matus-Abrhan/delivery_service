import enum
from .db import db

class OrderState(enum.Enum):
    Creating = "creating"
    Finalyzed = "finalyzed"
    Preparing = "preparing"
    Ready = "ready"
    Delivering = "delivering"
    Delivered = "delivered"
    Completed = "completed"

class DeliveryState(enum.Enum):
    Open = "open"
    Closed = "closed"

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('user_customer.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('user_restaurant.id'))
    delivery_id = db.Column(db.Integer, db.ForeignKey('user_delivery.id'))
    food_items = db.Column(db.String(1000))
    order_state = db.Column(db.Enum(OrderState))
    delivery_state = db.Column(db.Enum(DeliveryState))
    sum_total = db.Column(db.Integer)