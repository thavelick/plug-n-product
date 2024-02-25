from flask import Flask, render_template, request


def create_app():
    app = Flask(__name__)

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/sign-in")
    def signin():
        return render_template("signin.html")

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

    return app
