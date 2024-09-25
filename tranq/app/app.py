import os
from flask import Flask, g, current_app

from tranq.config import Config
from tranq.utils.db import get_db, close_db
from tranq.app.extensions import bcrypt
from tranq.app.views.db_views import db_views


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    bcrypt.init_app(app)

    @app.before_request
    def before_request():
        g.db = get_db(current_app.config['DATABASE'])

    app.register_blueprint(db_views)

    @app.teardown_appcontext
    def teardown_db(exception):
        close_db()

        if exception:
            print("An exception occurred:", exception)

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    return app
