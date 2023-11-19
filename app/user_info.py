from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from .db import db
from .auth import login_required
from .user_model import UserEnum, BaseUser
from .order_model import Order

bp = Blueprint('info', __name__, url_prefix='/user')

@bp.route('/info', methods=["GET"])
@login_required
def user_info():
    base_user = BaseUser.query.first()
    user_id = base_user.id
    orders = Order.query.filter(Order.customer_id == user_id).all()
    return render_template('user/info.html', user=base_user, orders=orders)