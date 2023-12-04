from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from .db import db
from .auth import login_required
from .user_model import UserEnum, BaseUser
from .order_model import Order

bp = Blueprint('info', __name__, url_prefix='/user')

@bp.route('/info', methods=["GET"])
@login_required
def user_info():
    orders = Order.query.filter_by(customer_id=g.user.id).all()
    return render_template('user/info.html', user=g.user, orders=orders)

@bp.route('/delete')
def user_delete():
    db.session.delete(g.user)
    db.session.commit()
    return redirect(url_for('auth.logout'))
