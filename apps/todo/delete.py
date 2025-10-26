"""
delete.py

todoのタスクを削除するモジュール
"""
from . import bp
from apps.common.decorators import login_required
from apps.todo.models import Task
from apps.extensions import db 
from flask import redirect, url_for


@bp.post('/delete_task/<int:id>')
@login_required
def delete_task(id):
    task = Task.query.get_or_404(id)
    try:
        db.session.delete(task)
        db.session.commit()
        return redirect(url_for('todo.todo_get'))
    except Exception as e:
        db.session.rollback()
        return f'There was an issue deleting your task: {e}', 500