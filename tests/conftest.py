"""
conftest.py

fixure（テストの前準備や後片付けを自動で行ってくれる仕組み）を定義。
・Flaskアプリを起動する
・テスト用データベースを初期化する
・テストユーザーを登録しておく
・終わったら後片付けする（DB削除など）
"""
"""
@pytest.fixture 
「この関数はテスト時に使う“準備済みオブジェクト”を返しますよ」という目印（登録）であり、
pytest が引数名を見て自動的にその関数を呼び出してくれる仕組み
yieldでtest関数に処理をわたし、終わり次第、yield以降の処理に戻る
"""
import pytest
from apps.app import create_app
from apps.extensions import db
from werkzeug.security import generate_password_hash

@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True #appをテストモードに設定
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.create_all()
        yield app #yield:ここでテスト本体に処理を渡す
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client() #テストで使うクライエント（ブラウザの状態）の作成

@pytest.fixture
def db_session(app):
    with app.app_context():
        yield db.session #db.sessionの情報をテスト関数に渡す

@pytest.fixture
def test_user(app):
    from apps.auth.models import User
    with app.app_context():
        user = User(username = "test_user", useremail="test@test.com", password_hash=generate_password_hash("1234") )
        db.session.add(user)
        db.session.commit()
        yield user
        db.session.delete(user)
        db.session.commit()
        
@pytest.fixture
def login_as(client,db_session):
    from apps.auth.models import User
    user = User(username="test_user", useremail="test_user@example.com",
                password_hash=generate_password_hash("pass"))
    db_session.add(user)
    db_session.commit()
    
    res = client.post("/auth/", data={"username":"test_user", "password":"1234"},
                      follow_redirects = True) #フォーム内の値。今のブラウザの状態に対して、postする
    assert res.status_code == 200
    with client.session_transaction() as sess:
        sess["userid"] = user.id

    return client,user

@pytest.fixture
def test_task(app,login_as,db_session):
    from datetime import date
    from apps.todo.models import Task
    client, user = login_as  
    task = Task(userid=user.id, content="test_content", due_date=date(2025, 11, 2))
    db_session.add(task)
    db_session.commit()
    return task

