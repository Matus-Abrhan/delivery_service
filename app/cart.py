from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from .db import db
from .auth import login_required
from .order_model import Order, OrderState
from .user_model import UserRestaurant

bp = Blueprint('cart', __name__, url_prefix='')

@bp.route('/cart', methods=('GET', 'POST'))
@login_required
def cart():
    if request.method == 'POST':
        error = None

        order = Order.query.filter_by(customer_id=g.user.id, order_state=OrderState.Creating).first()
        if not order:
            error = "No order to be payed"

        if error is None:
            restaurant = UserRestaurant.query.filter_by(id=order.restaurant_id).first()
            value = g.user.pay(restaurant, order.sum_total)
            if value == order.sum_total:
                # TODO: notify restaurant of the order
                order.order_state = OrderState.Finalyzed
                db.session.add(order)
                db.session.commit()

            return redirect(url_for('index'))
        
        flash(error)
        
    orders = Order.query.filter_by(customer_id=g.user.id)
    return render_template('user/cart.html', orders=orders)