from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from .auth import login_required
from .db import get_db

bp = Blueprint('user', __name__)

@bp.route('/')
@login_required
def index():
    db = get_db()
    users = db.execute(
        'SELECT username, id FROM user'
    ).fetchall()
    print(users[0]['username'])
    return render_template('user/index.html', users=users)
