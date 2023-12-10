from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from .db import db
from .auth import login_required
from .user_model import UserEnum
from .menu_model import Menu, FoodItem

bp = Blueprint('menu', __name__, url_prefix='/menu')

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create_menu():
    if g.user.user_type is not UserEnum.Restaurant:
        return redirect(url_for('index'))
    if request.method == 'POST':
        error = None

        if error is None:
            item_names = request.form.getlist('item_name[]')
            descriptions = request.form.getlist('description[]')
            prices = request.form.getlist('price[]')
            categories = request.form.getlist('category[]')
            print(categories)

            menu = Menu(restaurant_id=g.user.id)
            for i in range(len(item_names)):
                print("name: " + item_names[i] + ", cat: " + categories[i] + ", desc: " + descriptions[i] + ", price: " + prices[i])
                food_item = FoodItem(category=categories[i], name=item_names[i], description=descriptions[i], price=prices[i])
                menu.food_items.append(food_item)
            db.session.add(menu)
            db.session.commit()
            
            return redirect(url_for('index'))
        
        flash(error)
    
    return render_template('menu/create.html')