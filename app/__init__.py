from flask import Flask, render_template


def create_app():
    app = Flask(__name__)

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/sign-in")
    def signin():
        return render_template("signin.html")

    return app
