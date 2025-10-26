"""
logout.py

ログアウトを処理するモジュール
"""
from . import bp
from flask import session,redirect,flash,url_for


@bp.get('/logout')
def logout():
    # session.pop('user', None)
    session.clear()
    flash("ログアウトしました", "success")
    return redirect(url_for('auth.login_get'))
