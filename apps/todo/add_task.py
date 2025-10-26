"""
add_task.py

todoの追加を設定するモジュール
"""

from flask import request, render_template, url_for, session, redirect
from apps.common.decorators import login_required
from apps.todo.models import Task
from apps.extensions import db
from . import bp
from datetime import date

@bp.get("/add_task") 
@login_required
def add_task_get():
    return render_template("add_task.html")

@bp.post("/add_task")
@login_required
def add_task_post():
        content = request.form.get('content')
        due_date_str = request.form.get('due_date')

        try:
            userid = session.get('userid')
            due_date = date.fromisoformat(due_date_str)
            new_task = Task(userid=userid, content=content, due_date=due_date)

            db.session.add(new_task)
            db.session.commit()
            return redirect(url_for('todo.todo_get')) 
        except Exception as e:
            db.session.rollback()
            return f'There was an issue adding your task:{e}',500