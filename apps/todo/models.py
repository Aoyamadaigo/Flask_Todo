"""
todo/models.py

Todoタスクに関するデータベースモデルを定義するモジュール
extentions.pyで定義したdbを拡張して作成する。

"""
from apps.extensions import db

class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey(
        "users.id", name="fk_tasks_userid_users_id", ondelete="CASCADE"),
        nullable=True, index=True)  # 外部キーを作成するときの扱いに注意
    content = db.Column(db.String(200))
    due_date = db.Column(db.Date, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    user = db.relationship('User', back_populates="tasks")
