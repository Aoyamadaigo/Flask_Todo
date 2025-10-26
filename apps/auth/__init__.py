"""
auth/__init__.py

auth機能の初期化モジュール
Blueprintの初期設定と、対応するviewの読み込みを行う。
Flaskアプリ本体（app.py/create_app関数）からこのBluepritを登録して使用する。

"""

from flask import Blueprint

bp = Blueprint("auth", __name__, url_prefix="/auth", template_folder="templates")

from . import view_user,view_register,logout