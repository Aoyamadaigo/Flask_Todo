import os
from flask import Flask,redirect,url_for
from .extensions import db,migrate

def create_app():
    app = Flask(__name__)
    app.secret_key = 'login_secret_key'
    app.url_map.strict_slashes = False
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.sqlite"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app) #dbの初期化
    migrate.init_app(app, db)

    from apps import models

    from apps.auth import bp as auth_bp #apps内の各機能のブループリントを定義
    from apps.todo import bp as todo_bp
    app.register_blueprint(auth_bp) #各機能のブループリントを登録
    app.register_blueprint(todo_bp)

    @app.get("/")
    def root():
        return redirect(url_for("auth.login_get"))

    return app

