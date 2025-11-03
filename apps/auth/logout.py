"""
logout.py

ログアウトを処理するモジュール
"""
from . import bp
from flask import session,redirect,flash,url_for
from apps.common.decorators import login_required 

@bp.get('/logout')
@login_required
def logout():
    # session.pop('user', None)
    session.clear()
    flash("ログアウトしました", "success")
    return redirect(url_for('auth.login_get')) #url_forでredirectする場合、bp名.関数名でredirect先を定義
