"""
extensions.py

Flaskの機能を外にまとめるためのモジュール。
DBやMigrateの定義をここで行い、
models.py では DB の利用だけを行う。
"""

import sqlite3
from sqlalchemy.engine import Engine
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event,MetaData
from flask_migrate import Migrate


# naming_convention：制約に自動で名前を付ける
# username = db.Column(db.String(64), unique=True)　→　uq_users_usernameと名前が付く
# 付けておくことで、マイグレートごとの差分発生を防げる
convention = {
    "ix": "ix_%(table_name)s_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)
migrate = Migrate(directory="apps/migrations") 


# SQLiteで外部キー制約を有効にする


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
