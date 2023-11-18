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
            # TODO: add ui for creating food menues
            menu = Menu(restaurant_id=g.user.id, food_items=[FoodItem(name='food1', price=5), FoodItem(name='food2', price=10)])
            db.session.add(menu)
            db.session.commit()
            
            return redirect(url_for('index'))
        
        flash(error)
    
    return render_template('menu/create.html')