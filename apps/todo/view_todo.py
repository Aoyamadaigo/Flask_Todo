"""
view_todo.py

todoの初期画面を設定するモジュール
各機能(user，todo)の初期画面はview関数で定義。
__init__ファイルでbpで定義を行い、トップ画面のURLである"/"でルートを定義
"""

from flask import render_template,session
from apps.common.decorators import login_required
from . import bp
from apps.todo.models import Task

@bp.get("/",endpoint="todo_get") #todo/bpからimportしているので、"/"で設定。Flaskのルーティングは「URL + HTTPメソッド」で区別される
@login_required
def todo_get():
    tasks = Task.query.filter_by(userid = session['userid']).all()
    return render_template("index.html", tasks=tasks)

