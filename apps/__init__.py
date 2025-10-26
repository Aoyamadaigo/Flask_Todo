import os
from flask import Flask,redirect,url_for
from .extensions import db,migrate

def create_app():
    app = Flask(__name__)
    app.secret_key = 'login_secret_key'
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.sqlite"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate.init_app(app, db)

    from apps import models

    from apps.auth import bp as auth_bp
    from apps.todo import bp as todo_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(todo_bp)

    @app.get("/")
    def root():
        return redirect(url_for("auth.login_get"))

    return app

