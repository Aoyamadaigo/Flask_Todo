"""
toggle_complete.py

todoタスクの完了，未完了を切り替えるモジュール
"""

from . import bp
from apps.common.decorators import login_required
from  apps.todo.models import Task
from apps.extensions import db
from flask import redirect, url_for

@bp.post('/toggle_complete/<int:id>')
@login_required
def toggle_complete(id):
    task = Task.query.get_or_404(id)
    task.completed = not task.completed
    try:
        db.session.commit()
        return redirect(url_for("todo.todo_get"))
    except Exception as e:
        db.session.rollback()
        return 'There was an issue adding your task'