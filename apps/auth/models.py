"""
auth/models.py

ユーザー情報のデータベースモデルを定義したモジュール
extensions.pyで定義したdbを利用してテーブルを作成する。

"""

from apps.extensions import db

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False,
                         unique=True, index=True)
    useremail = db.Column(db.String(64), nullable=False,
                          unique=True, index=True)
    password_hash = db.Column(db.String(128),nullable=False)
    administrator = db.Column(db.Boolean, default=False)
    tasks = db.relationship('Task', back_populates="user",
                            cascade="all,delete-orphan", passive_deletes=True)