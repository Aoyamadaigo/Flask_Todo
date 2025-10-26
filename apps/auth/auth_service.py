"""
auth_service.py

view_user.pyで使用するユーザー認証を処理するモジュール
"""

from apps.auth.models import User
from werkzeug.security import check_password_hash 

def auth_service(username:str, password:str):
        user = User.query.filter_by(username=username).first()
        if not user:
            return None, "ユーザーが登録されていません"
        
        if user and check_password_hash(user.password_hash, password):
            return user,None
        else:
            return None, None
                
            