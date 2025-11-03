"""
decorators.py

アプリ全体で使うデコレーター関数をまとめるモジュール。
"""

from functools import wraps
from flask import session, request, redirect,url_for, g



def login_required(f):
    @wraps(f) #wrapper関数
    def wrapper(*args, **kwargs):
        """
        ログインしていないユーザーが保護されたページにアクセスした場合、
        ログイン画面にリダイレクトする。
        """
        userid = session.get('userid')
        if not userid:
            from urllib.parse import quote
            next_url = quote(request.path or '/') #アクセスしたURLがあれば、取得。なければ、トップを取得する。
            return redirect(url_for('auth.login_get',next=next_url)) #next：ネストが深くても、ログイン後、目的のURLにすぐ行ける
        g.current_user_id = userid #g:リクエスト中だけ有効なグローバル変数
        return f(*args, **kwargs)
    return wrapper
