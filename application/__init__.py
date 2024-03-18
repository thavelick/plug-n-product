import os
from flask import (
    Flask,
    g,
    session,
)
from . import auth, db
from .htmx_tools import render_htmx_template
from .models import User


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, "app.sqlite"),
        SECRET_KEY="KnoX5LcT5wnaxDNYiW0vdJQhUW6NU",  # Just for development
    )

    if not test_config:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    app.register_blueprint(auth.bp)

    @app.route("/")
    def index():
        return render_htmx_template("index.html", "content")

    @app.route("/pricing")
    def pricing():
        return render_htmx_template("pricing.html", "content")

    @app.before_request
    def load_logged_in_user():
        user_id = session.get("user_id")
        g.user = User.get(user_id)

    db.init_app(app)
    return app
