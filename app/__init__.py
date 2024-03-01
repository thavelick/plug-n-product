import os
from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash
from . import db


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, "app.sqlite"),
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

    @app.route("/sign-in", methods=["GET", "POST"])
    def signin():
        if request.method == "POST":
            email = request.form["email"]
            password = request.form["password"]

            connection = db.get_db_connection()
            user = connection.execute(
                "SELECT * FROM user WHERE email = ?", (email,)
            ).fetchone()
            if user and check_password_hash(user["password"], password):
                session.clear()
                session["user_id"] = user["id"]
                return redirect(url_for("index"))

            flash("Error! Please try again.")

        return render_template("signin.html", email=request.form.get("email", ""))

    @app.route("/sign-in/password", methods=["POST"])
    def signin_password():
        password_input_type = "password"
        if request.form.get("show_password") == "on":
            password_input_type = "text"
        return render_template(
            "signin_password.html",
            password_input_type=password_input_type,
            password=request.form.get("password", ""),
        )

    db.init_app(app)
    return app
