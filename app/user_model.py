from flask import Blueprint, flash, redirect, render_template, request, url_for
from sqlalchemy import Integer, String
import enum

from .db import db

class UserEnum(enum.Enum):
    Delivery = "delivery"
    Customer = "customer"
    Restaurant = "restaurant"

class BaseUser(db.Model):
    #__abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(100), nullable=False)
    wallet = db.Column(db.Integer)
    user_type = db.Column(db.Enum(UserEnum))

    def __init__(self, **kwargs):
        for (k, v) in kwargs.items():
            setattr(self, k, v)


    def pay(self, dest_user, value: int):
        error = None

        if not isinstance(dest_user, BaseUser):
            error = f"Unexpected type for User, {type(dest_user)}"
        if value < 0:
            error = f"Value {value} not allowed"
        if self.wallet < value:
            error = f"Unsufficient funds!"
        
        if error is None:
            dest_user = BaseUser.query.filter_by(id=dest_user.id).first()

            self.wallet -= value
            dest_user.wallet += value
            db.session.add_all([
                self, 
                dest_user
            ])
            db.session.commit()
            
            return value
        flash(error)
        return None

class UserCustomer(BaseUser):
    id = db.Column(db.Integer, db.ForeignKey('base_user.id'), primary_key=True)

    def __init__(self, **kwargs):
        super().__init__(user_type=UserEnum.Customer, **kwargs)

class UserRestaurant(BaseUser):
    id = db.Column(db.Integer, db.ForeignKey('base_user.id'), primary_key=True)
    menu = db.relationship("Menu")

    def __init__(self, **kwargs):
        super().__init__(user_type=UserEnum.Restaurant, **kwargs)


class UserDelivery(BaseUser):
    id = db.Column(db.Integer, db.ForeignKey('base_user.id'), primary_key=True)

    def __init__(self, **kwargs):
        super().__init__(user_type=UserEnum.Delivery, **kwargs)
