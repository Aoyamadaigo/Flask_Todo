"""
todo/__init__.py

todo機能の初期化モジュール
Blueprint機能の初期設定と必要なview関数の読み込みを行う（各機能フォルダの__init__ファイルで設定）
app.py/create_app関数で登録して使用する
"""

from flask import Blueprint

bp = Blueprint('todo',__name__, url_prefix="/todo", template_folder="templates")
from . import view_todo,add_task,delete,toggle_complete #todo内で使う全ての機能の登録が必須