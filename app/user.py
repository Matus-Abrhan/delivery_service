from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from .db import db
from .auth import login_required
from .menu_model import Menu, FoodItem
from .order_model import Order, OrderState
from .user_model import UserEnum

@bp_root.route('/', methods=('GET', 'POST'))
@login_required
def index():
    if request.method == 'POST': 
        if g.user.user_type is UserEnum.Customer:
            food_item_id = request.form['food_item_id']

            error = None
            food_item = FoodItem.query.filter_by(id=food_item_id).first()
            menu = Menu.query.filter_by(id=food_item.menu_id).first()
            order = Order.query.filter_by(customer_id=g.user.id, order_state=OrderState.Composing).first()
            if order is None:
                order = Order(customer_id=g.user.id, restaurant_id=menu.restaurant_id, food_items='', sum_total=0, order_state=OrderState.Composing)
            if order.restaurant_id != menu.restaurant_id:
                error = 'Different Restaurant is already used'

            order.food_items += food_item.name + "," 
            order.sum_total += food_item.price

            if error is None:
                db.session.add(order)
                db.session.commit()
                return redirect(url_for('index'))
            
            flash(error)
        elif g.user.user_type is UserEnum.Restaurant:
            order_id = request.form['order_id']

            error = None
            order = Order.query.filter_by(id=order_id),first()
            if order.restaurant_id != g.user.user_id:
                error = 'Order doesnt belong to this restaurant'
            if order.order_state != OrderState.Preparing:
                error = 'Wrong order state, cannot finalyze order'
            
            if error is None:
                order.order_state = OrderState.Delivering
                # TODO


    # TODO: add practical way to add items to cart
    if g.user.user_type is UserEnum.Restaurant():
        orders = Order.query.filter_by(restaurant_id=g.user.id).all()
        return render_template('auth/index_restaurent.html', orders=orders)
    else:
        menus = Menu.query.all()
        return render_template('auth/index.html', menus=menus)