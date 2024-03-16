import functools
import os
from jinja2_fragments.flask import render_block
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

    def require_logged_out(view):
        @functools.wraps(view)
        def wrapped_view(**kwargs):
            if g.user:
                flash("You are already signed in.", "warning")
                return redirect(url_for("index"))
            return view(**kwargs)

        return wrapped_view

    def oob_block_tag(template, block, tag_name, tag_id, **kwargs):
        content = render_block(template, block, **kwargs)
        return f'<{tag_name} id="{tag_id}" hx-swap-oob="true">{content}</{tag_name}>'

    def render_htmx_template(template, block, **kwargs):
        if request.headers.get("HX-Request"):
            blocks = [
                render_block(template, block, **kwargs),
                oob_block_tag(
                    template, block="title", tag_name="title", tag_id="title", **kwargs
                ),
                oob_block_tag(
                    "base.html",
                    block="flash_messages",
                    tag_name="div",
                    tag_id="flash_messages",
                    **kwargs,
                ),
            ]
            if "top_nav" in session.get("oob_updates", []):
                blocks.append(
                    oob_block_tag(
                        "base.html",
                        block="top_nav",
                        tag_name="nav",
                        tag_id="top_nav",
                        **kwargs,
                    )
                )
            session.pop("oob_updates", None)
            return " ".join(blocks)

        return render_template(template, **kwargs)

    @app.route("/")
    def index():
        return render_htmx_template("index.html", "content")

    @app.route("/register", methods=["GET", "POST"])
    @require_logged_out
    def register():
        if request.method == "POST":
            email = request.form["email"]
            password = request.form["password"]
            try:
                User.create(email, password)
            except UserCreationError as error:
                flash(str(error), "error")
            else:
                flash("You have successfully registered! Please sign in.", "success")
                return redirect(url_for("signin"))
        return render_htmx_template(
            "register.html", "content", email=request.form.get("email", "")
        )

    @app.route("/sign-in", methods=["GET", "POST"])
    @require_logged_out
    def signin():
        if request.method == "POST":
            email = request.form["email"]
            password = request.form["password"]

            user = User.authenticate(email, password)
            if user:
                session.clear()
                session["user_id"] = user.id
                session["oob_updates"] = ["top_nav"]
                return redirect(url_for("index"))

            flash(
                "Error! Could not sign in. Please check your credentials and try again.",
                "error",
            )

        return render_htmx_template(
            "signin.html", "content", email=request.form.get("email", "")
        )

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
        session["oob_updates"] = ["top_nav"]
        return redirect(url_for("index"))

    @app.before_request
    def load_logged_in_user():
        user_id = session.get("user_id")
        g.user = User.get(user_id)

    db.init_app(app)
    return app
