import os
from flask import Flask, redirect, url_for, jsonify
from .extensions import db, migrate
from sqlalchemy import text  # ★

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY", "login_secret_key")
    app.url_map.strict_slashes = False

    base_dir = os.path.dirname(os.path.abspath(__file__))
    database_url = os.getenv("DATABASE_URL", f"sqlite:///{os.path.join(base_dir, 'todo.sqlite')}")
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql+psycopg2://", 1)

    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.logger.info(f"Using DB: {database_url}")

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

    @app.get("/__health")
    def health():
        try:
            db.session.execute(text("SELECT 1"))
            return jsonify(ok=True)
        except Exception as e:
            app.logger.exception("DB health check failed")  
            return jsonify(ok=False, error=str(e)), 500

    @app.errorhandler(Exception)
    def handle_all(e):
        from werkzeug.exceptions import HTTPException
        if isinstance(e, HTTPException):
            # 404などはそのまま
            return e
        app.logger.exception("Unhandled exception")
        return jsonify(error="internal server error"), 500

    return app
