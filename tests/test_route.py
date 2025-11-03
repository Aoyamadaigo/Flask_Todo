"""
test_routes.py

ログイン，未ログイン時の
URLへのアクセスやレスポンスを確認するユニットテスト
(ログイン，ルーティング確認)
"""
class TestRouting:

    def test_login_page(self, client):
        res = client.get("/auth/")
        html = res.data.decode("utf-8")
        assert res.status_code == 200
        assert "ログイン" in html

    def test_register_page(self, client):
        res = client.get("/auth/register/")
        html = res.data.decode("utf-8")
        assert res.status_code == 200
        assert "新規ユーザー登録" in html
        
    def test_todo_list(self, client):
        res = client.get("/todo/")
        assert res.status_code == 302
        assert res.headers["Location"] == "/auth/?next=/todo"

    def test_todo__list_after_user_login(self,login_as):
        res = login_as.get("/todo/")
        html = res.data.decode("utf-8")
        assert not "ログイン" in html
        assert  "Todo List" in html

    def test_add_task(self,client):
        res = client.get("/todo/add_task/")
        assert res.status_code == 302
        assert res.headers["Location"]  == "/auth/?next=/todo/add_task"

    def test_add_task_after_login(self,login_as):
        res = login_as.get("/todo/add_task/")
        html = res.data.decode("utf-8")
        assert not "ログイン" in html
        assert "タスク内容" in html

    def test_logout(self,client):
        res = client.get("/auth/logout/")
        assert res.status_code == 302
        assert res.headers["Location"] == "/auth/?next=/auth/logout"

    def test_logout_after_login(self, login_as):
        res = login_as.get("/auth/logout/", follow_redirects=True)
        assert res.status_code == 200

    def test_not_login(self,test_user,client):
        res = client.post("/auth/", 
                          data={"username":"not_regist_user","password":"not_register_pass"},
                          follow_redirects =True)
        html = res.data.decode("utf-8")
        assert "ユーザーが登録されていません" in html
        
        assert res.status_code == 200
        assert "ログイン" in html
 
