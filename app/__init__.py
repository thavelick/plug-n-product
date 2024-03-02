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
from werkzeug.security import check_password_hash, generate_password_hash
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

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            email = request.form["email"]
            password = request.form["password"]
            connection = db.get_db_connection()
            error = None

            if not email:
                error = "Email is required."
            elif not password:
                error = "Password is required."
            elif len(password) < 10:
                error = "Password must be at least 10 characters long."

            if not error:
                try:
                    connection.execute(
                        "INSERT INTO user (email, password) VALUES (?, ?)",
                        (email, generate_password_hash(password)),
                    )
                    connection.commit()
                except connection.IntegrityError:
                    error = "Sorry that account is already registered. Please sign in."
                else:
                    return redirect(url_for("signin"))

            flash(error, "error")

        return render_template("register.html", email=request.form.get("email", ""))

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

            flash(
                "Error! Could not sign in. Please check your credentials and try again.",
                "error",
            )

        return render_template("signin.html", email=request.form.get("email", ""))

    @app.route("/register/password", methods=["POST"])
    @app.route("/sign-in/password", methods=["POST"])
    def signin_password():
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

        if user_id is None:
            g.user = None
        else:
            g.user = (
                db.get_db_connection()
                .execute("SELECT * FROM user WHERE id = ?", (user_id,))
                .fetchone()
            )

    db.init_app(app)
    return app
