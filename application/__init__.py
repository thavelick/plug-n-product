import os
from flask import (
    Flask,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from . import db
from .models import User, UserCreationError


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

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            email = request.form["email"]
            password = request.form["password"]
            try:
                User.create(email, password)
            except UserCreationError as error:
                flash(str(error), "error")
            else:
                return redirect(url_for("signin"))
        return render_template("register.html", email=request.form.get("email", ""))

    @app.route("/sign-in", methods=["GET", "POST"])
    def signin():
        if request.method == "POST":
            email = request.form["email"]
            password = request.form["password"]

            user = User.authenticate(email, password)
            if user:
                session.clear()
                session["user_id"] = user.id
                return redirect(url_for("index"))

            flash(
                "Error! Could not sign in. Please check your credentials and try again.",
                "error",
            )

        return render_template("signin.html", email=request.form.get("email", ""))

    @app.route("/register/password", methods=["POST"])
    @app.route("/sign-in/password", methods=["POST"])
    def password_field():
        password_input_type = "password"
        if request.form.get("show_password") == "on":
            password_input_type = "text"
        return render_template(
            "password_field.html",
            password_input_type=password_input_type,
            password=request.form.get("password", ""),
        )

    @app.route("/logout")
    def logout():
        session.clear()
        return redirect(url_for("index"))

    @app.before_request
    def load_logged_in_user():
        user_id = session.get("user_id")
        g.user = User.get(user_id)

    db.init_app(app)
    return app
