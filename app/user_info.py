from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from .db import db
from .auth import login_required
from .user_model import UserEnum, BaseUser

bp = Blueprint('info', __name__, url_prefix='/user')

@bp.route('/info', methods=["GET"])
@login_required
def user_info():
    base_user = BaseUser.query.first()
    return render_template('user/info.html', user=base_user)