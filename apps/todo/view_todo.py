"""
view_todo.py

todoの初期画面を設定するモジュール
"""

from flask import render_template,session
from apps.common.decorators import login_required
from . import bp
from apps.todo.models import Task

@bp.get("/") #todo/bpからimportしているので、"/"で設定。Flaskのルーティングは「URL + HTTPメソッド」で区別される
@login_required
def todo_get():
    tasks = Task.query.filter_by(userid = session['userid']).all()
    return render_template("index.html", tasks=tasks)

