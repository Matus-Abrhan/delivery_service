from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from .db import db
from .auth import login_required
from .menu_model import Menu, FoodItem
from .order_model import Order, OrderState, DeliveryState
from .user_model import UserEnum, BaseUser


bp_root = Blueprint('index', __name__, url_prefix='/')

@bp_root.route('/', methods=('GET', 'POST'))
@login_required
def index():
    if request.method == 'POST': 
        if g.user.user_type is UserEnum.Customer:
            food_item_id = request.form.get('food_item_id', None)
            quantity = request.form.get('quantity', None)

            error = None

            food_item = FoodItem.query.filter_by(id=food_item_id).first()
            menu = Menu.query.filter_by(id=food_item.menu_id).first()
            order = Order.query.filter_by(customer_id=g.user.id, order_state=OrderState.Creating).first()
            if order is None:
                order = Order(customer_id=g.user.id, restaurant_id=menu.restaurant_id, 
                food_items='', sum_total=0, order_state=OrderState.Creating, delivery_state=DeliveryState.Open)
            if order.restaurant_id != menu.restaurant_id:
                error = 'Different Restaurant is already used'

            for i in range(int(quantity)):
                order.food_items += food_item.name + ","
                order.sum_total += food_item.price

            if error is None:
                db.session.add(order)
                db.session.commit()
                return redirect(url_for('index'))
            
            flash(error)

        elif g.user.user_type is UserEnum.Restaurant:
            order_id_take = request.form.get('order_id_take', None)
            order_id_ready = request.form.get('order_id_ready', None)

            error = None
            if order_id_take is not None:
                order = Order.query.filter_by(id=order_id_take).first()
                if order.restaurant_id != g.user.id:
                    error = 'Order doesnt belong to this restaurant'
                elif order.order_state != OrderState.Finalyzed:
                    error = 'Wrong order state, cannot take order'
                
                if error is None:
                    order.order_state = OrderState.Preparing
                    db.session.add(order)
                    db.session.commit()
                    return redirect(url_for('index'))
                
                flash(error)
            
            elif order_id_ready is not None:
                order = Order.query.filter_by(id=order_id_ready).first()
                if order.restaurant_id != g.user.id:
                    error = 'Order doesnt belong to this restaurant'
                elif order.order_state != OrderState.Preparing or order.delivery_state != DeliveryState.Closed:
                    error = 'Wrong order state, cannot mark as ready'
                
                if error is None:
                    order.order_state = OrderState.Ready
                    db.session.add(order)
                    db.session.commit()
                    return redirect(url_for('index'))

                flash(error)
        
        elif g.user.user_type is UserEnum.Delivery:
            order_id_take = request.form.get('order_id_take', None)
            order_id_pickup = request.form.get('order_id_pickup', None)
            order_id_delivered = request.form.get('order_id_delivered', None)

            error = None

            if order_id_take is not None:
                order = Order.query.filter_by(id=order_id_take).first()
                if order.order_state != OrderState.Preparing:
                    error = 'Wrong order state, cannot take order'
                elif order.delivery_state != DeliveryState.Open:
                    error = "Order not open for delivery"

                if error is None:
                    order.delivery_id = g.user.id
                    order.delivery_state = DeliveryState.Closed
                    db.session.add(order)
                    db.session.commit()
                    return redirect(url_for('index'))

                flash(error)
            
            elif order_id_pickup is not None:
                order = Order.query.filter_by(id=order_id_pickup).first()
                if order.order_state != OrderState.Ready:
                    error = 'Wrong order state, cannot pickup order'

                if error is None:
                    lat = request.form.get("latitude", None)
                    long = request.form.get("longitude", None)
                    order.order_state = OrderState.Delivering
                    order.longitude = long
                    order.latitude = lat
                    db.session.add(order)
                    db.session.commit()
                    return redirect(url_for('index'))

                flash(error)
            
            elif order_id_delivered is not None:
                order = Order.query.filter_by(id=order_id_delivered).first()

                if order.order_state != OrderState.Delivering:
                    error = 'Wrong order state, mark as delivered'

                if error is None:
                    order.order_state = OrderState.Delivered
                    db.session.add(order)
                    db.session.commit()
                    return redirect(url_for('index'))

                flash(error)

    # TODO: add practical way to add items to cart
    if g.user.user_type is UserEnum.Restaurant:
        orders = Order.query.filter_by(restaurant_id=g.user.id).all()
        return render_template('auth/index_restaurant.html', orders=orders)

    elif g.user.user_type is UserEnum.Customer:
        restaurants = {restaurant.username for restaurant in BaseUser.query.filter_by(user_type=UserEnum.Restaurant)}
        categories = {food_item.category for food_item in FoodItem.query.all()}

        category = request.args.get('category', None)
        restaurant = request.args.get('restaurant', None)
        

        if category and restaurant:
            restaurant = BaseUser.query.filter_by(username=restaurant).first()
            menus = Menu.query.filter_by(restaurant_id=restaurant.id).all()
            food_items = []
            for menu in menus:
                food_items += FoodItem.query.filter_by(id=menu.id, category=category).all()
        elif category:
            food_items = FoodItem.query.filter_by(category=category).all()
        elif restaurant:
            print(restaurant)
            restaurant = BaseUser.query.filter_by(username=restaurant).first()
            print(restaurant)
            menus = Menu.query.filter_by(restaurant_id=restaurant.id).all()
            print(menus)
            food_items = []
            for menu in menus:
                food_items += FoodItem.query.filter_by(menu_id=menu.id).all()
            print(food_items)
        else:
            food_items = FoodItem.query.all()
        return render_template('auth/index.html',categories=categories, restaurants=restaurants, food_items=food_items)

    elif g.user.user_type is UserEnum.Delivery:
        available_orders = Order.query.filter_by(order_state=OrderState.Preparing, delivery_state=DeliveryState.Open).all()
        taken_orders = Order.query.filter_by(delivery_id=g.user.id, delivery_state=DeliveryState.Closed)
        return render_template('auth/index_delivery.html', available_orders=available_orders, taken_orders=taken_orders)


@bp_root.route('newLocation', methods=['POST'])
@login_required
def update_location():
    data = request.get_json()
    latitude = data['latitude']
    longitude = data['longitude']
    orders = Order.query.filter_by(delivery_id=g.user.id, order_state=OrderState.Delivering).all()
    for order in orders:
        order.longitude = longitude
        order.latitude = latitude
        db.session.add(order)
        db.session.commit()
    return redirect(url_for('index'))
