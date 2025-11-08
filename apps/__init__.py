import os
from flask import Flask, redirect, url_for
from .extensions import db, migrate

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY", "login_secret_key")
    app.url_map.strict_slashes = False

    # ===== DB 設定：本番は DATABASE_URL、なければローカルのSQLite =====
    base_dir = os.path.dirname(os.path.abspath(__file__))
    database_url = os.getenv("DATABASE_URL", f"sqlite:///{os.path.join(base_dir, 'todo.sqlite')}")

    # Render/Heroku系の "postgres://" を SQLAlchemy 形式へ補正
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql+psycopg2://", 1)

    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate.init_app(app, db)

    # モデルをAlembicに認識させる
    from . import models

    # Blueprints
    from apps.auth import bp as auth_bp
    from apps.todo import bp as todo_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(todo_bp)

    @app.get("/")
    def root():
        return redirect(url_for("auth.login_get"))

    return app
