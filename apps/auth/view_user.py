"""
view_user.py

login.htmlからフォームの情報を受け取り、ログインに成功した場合、
ログイン画面にリダイレクトするモジュール。
ユーザー認証はauth_service.pyで処理する。
"""


from flask import Blueprint,request, render_template, session, flash, redirect, url_for
from apps.auth.models import User
from apps.auth.auth_service import auth_service
from apps.extensions import db
from . import bp


@bp.get("/")
def login_get():
    return render_template("login.html")    

@bp.post("/")
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    next_url = request.args.get('next')
    try:
        user, error = auth_service(username, password)
        if user:
            session['userid'] = user.id  # セッションでidに関する情報も格納
            session['user'] = user.username
            flash(f"{username}でログインしました", "success")
            return redirect(next_url or url_for('todo.todo_get'))
        else:
            flash(error, "error")
            return redirect(url_for('auth.login_get'))
            
    except Exception as e:  # Exception as eでエラー内容を格納
        db.session.rollback()
        flash(f"ログイン処理でエラー:{e}", "error")
        return redirect(url_for("auth.login_get"))
            

