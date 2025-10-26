"""
register_service.py

sign_up.py（ユーザー登録モジュール）で使用するユーザー存在確認を
するためのモジュール
"""
from apps.auth.models import User
from sqlalchemy import or_


def register_service(username:str, email: str):

    dup = User.query.filter(or_(User.username == username,
                        User.useremail == email)).first()
    if dup:
        if dup.username == username:
            return dup, "すでにこの名前のユーザーは存在します"
        elif dup.useremail == email:
            return dup, "すでにこのemailのユーザーは存在します"
        
    return None, None