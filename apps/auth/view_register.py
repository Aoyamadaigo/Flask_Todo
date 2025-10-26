"""
sign_up.py

新規ユーザーの登録を行うためのモジュール
"""
from flask import request, flash, redirect ,url_for,render_template
from . import bp
from apps.extensions import db
from .register_service import register_service
from werkzeug.security import generate_password_hash
from apps.auth.models import User

@bp.get("/register")
def register_get():
    return render_template("register.html")


@bp.post("/register")
def register_post():
    username = request.form.get('username','').strip()
    password = request.form.get('password','').strip()
    email = request.form.get('email','').strip()


    if not username or not password or not email:
        flash("ユーザー名，パスワード，emailは必須項目です","error")
        return redirect(url_for('auth.register_get'))

    dup,error = register_service(username=username, email=email)

    if dup:
        flash(error, 'error')
        return redirect(url_for('auth.login_get'))
    
    else:
        try:
            hashed_password = generate_password_hash(password)
            new_user = User(username=username,
                                    password_hash=hashed_password, useremail=email)
            db.session.add(new_user)
            db.session.commit()
            flash('ユーザー登録に成功しました', 'success')
            return redirect(url_for("auth.login_get"))

        except Exception as e:
            db.session.rollback()
            flash(f"ユーザー登録でエラーが起きました:{e}", "error")  # flashはflaskでメッセージ表示する機能
            return redirect(url_for('auth.register_get'))


                
