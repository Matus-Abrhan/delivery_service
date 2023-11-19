from flask import Flask


from .db import db
from .auth import bp
from .menu import bp
from .cart import bp
from .user import index, bp_root
import os

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(app.instance_path, 'app.sqlite')
    )

    app.config.from_object('config.Dev')

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    app.register_blueprint(user.bp_root)
    app.register_blueprint(auth.bp)
    app.register_blueprint(menu.bp)
    app.register_blueprint(cart.bp)

    app.add_url_rule('/', view_func=index)
    db.init_app(app)
    with app.app_context():
        db.create_all()

    return app
