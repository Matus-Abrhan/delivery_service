import functools

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from .db import db
from .user_model import BaseUser, UserCustomer, UserDelivery, UserRestaurant, UserEnum
from .menu_model import Menu, FoodItem
from .order_model import Order, OrderState

bp = Blueprint('auth', __name__, url_prefix='/auth')
bp_root = Blueprint('index', __name__, url_prefix='/')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        user_type = request.form['user_type']

        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            if user_type == UserEnum.Customer.value:
                user = UserCustomer(username=username, password=password, wallet=10)
            elif user_type == UserEnum.Restaurant.value:
                user = UserRestaurant(username=username, password=password, wallet=100)
            elif user_type == UserEnum.Delivery.value:
                user = UserDelivery(username=username, password=password, wallet=0)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        error = None
        user = BaseUser.query.filter_by(username=username).first()

        if user is None:
            error = 'Incorrect username or password.'
        elif check_password_hash(password, user.password):
            error = 'Incorrect username or password.'

        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = BaseUser.query.filter_by(id=user_id).first()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
