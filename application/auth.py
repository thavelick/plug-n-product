import functools
from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    url_for,
    render_template,
    request,
    session,
)
from .htmx_tools import render_htmx_template
from .models import User, UserCreationError


bp = Blueprint("auth", __name__, url_prefix="/auth")


def require_logged_out(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user:
            flash("You are already signed in.", "warning")
            return redirect(url_for("index"))
        return view(**kwargs)

    return wrapped_view


@bp.route("/register", methods=["GET", "POST"])
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
            return redirect(url_for("auth.signin"))
    return render_htmx_template(
        "register.html", "content", email=request.form.get("email", "")
    )


@bp.route("/sign-in", methods=["GET", "POST"])
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


@bp.route("/logout")
def logout():
    session.clear()
    session["oob_updates"] = ["top_nav"]
    return redirect(url_for("index"))


@bp.route("/password-field", methods=["POST"])
def password_field():
    password_input_type = "password"
    if request.form.get("show_password") == "on":
        password_input_type = "text"
    return render_template(
        "password_field.html",
        password_input_type=password_input_type,
        password=request.form.get("password", ""),
    )
