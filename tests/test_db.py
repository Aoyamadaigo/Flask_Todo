"""
test_db.py

db関連のユニットテスト（データ追加・削除など）
(ログイン，ルーティング確認)
"""
from werkzeug.security import generate_password_hash
from apps.extensions import db

class TestDB:

    """ユーザー登録確認"""
    def test_register_page_post(self,client,db_session):
        res = client.post("/auth/register",
                          data={"username":"testuser","email":"testmail@test.com","password":"1234"},
                          follow_redirects=True)
        html = res.data.decode("utf-8")
        assert res.status_code == 200
        assert "ログイン" in html

        from apps.auth.models import User
        user = db_session.query(User).filter_by(username = "testuser").first()
        assert user is not None

    """タスクの追加確認"""
    def test_add_task_post(self,db_session,login_as):
        client,user =login_as
        res = client.post("/todo/add_task/",
                      data={"content":"test_content","due_date":"2025-11-02"},
                      follow_redirects=True)
        assert res.status_code == 200
        
        from apps.todo.models import Task 
        task = db_session.query(Task).filter_by(content = "test_content").first()
     
        assert task is not None

    """タスクの削除確認"""
    def test_delete_task_post(self,login_as,test_task,db_session):
        client,user =login_as
        assert test_task.userid == user.id

        res = client.post(f"/todo/delete_task/{test_task.id}/", follow_redirects=True)
       
        from apps.todo.models import Task
        task = db_session.query(Task).filter_by(content = "test_content").first()
        assert task is None

    "ユーザーの重複登録確認"
    def test_double_user_check(self,client,test_user):
        res = client.post("/auth/register/", 
                          data = {"username":"test_user","email":"test@test.com","password":"1234"},
                          follow_redirects=True)
        assert res.status_code == 200
        html = res.data.decode("utf-8")
        print(html)
        assert not "新規登録する" in html
        assert  "すでにこの名前のユーザーは存在します" in html
        
        
        
        
        
        