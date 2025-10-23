import sqlite3
from sqlalchemy.engine import Engine
from sqlalchemy import event, MetaData, or_
from flask import Flask, render_template, redirect, request, url_for, session, flash, g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import date
from werkzeug.security import generate_password_hash,check_password_hash
from functools import wraps

# naming_convention：制約に自動で名前を付ける
# username = db.Column(db.String(64), unique=True)　→　uq_users_usernameと名前が付く
# 付けておくことで、マイグレートごとの差分発生を防げる
convention = {
    "ix": "ix_%(table_name)s_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)
migrate = Migrate()

app = Flask(__name__)
app.secret_key = 'login_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# バインド
db.init_app(app)
migrate.init_app(app, db)


# SQLiteで外部キー制約を有効にする


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False,
                         unique=True, index=True)
    useremail = db.Column(db.String(64), nullable=False,
                          unique=True, index=True)
    password_hash = db.Column(db.String(128),nullable=False)
    administrator = db.Column(db.Boolean, default=False)
    tasks = db.relationship('Task', back_populates="user",
                            cascade="all,delete-orphan", passive_deletes=True)

    
    


class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey(
        "users.id", name="fk_tasks_userid_users_id", ondelete="CASCADE"),
        nullable=True, index=True)  # 外部キーを作成するときの扱いに注意
    content = db.Column(db.String(200))
    due_date = db.Column(db.Date, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    user = db.relationship('User', back_populates="tasks")

def login_required(f):
    @wraps(f) #wrapper関数
    def wrapper(*args, **kwargs):
        userid = session.get('userid')
        if not userid:
            from urllib.parse import quote
            next_url = quote(request.path or '/') #アクセスしたURLがあれば、取得。なければ、トップを取得する。
            return redirect(url_for('login',next=next_url)) #next：ネストが深くても、ログイン後、目的のURLにすぐ行ける
        g.current_user_id = userid #g:リクエスト中だけ有効なグローバル変数
        return f(*args, **kwargs)
    return wrapper

# 初期画面


@app.route("/")
@login_required
def index():
    tasks = Task.query.filter_by(userid = session['userid']).all()
    return render_template("index.html", tasks=tasks)

# タスク追加画面


@app.route('/add_task', methods=['GET', 'POST'])
@login_required
def add_task():
    if request.method == 'POST':
        content = request.form.get('content')
        due_date_str = request.form.get('due_date')

        try:
            userid = session.get('userid')
            due_date = date.fromisoformat(due_date_str)
            new_task = Task(userid=userid, content=content, due_date=due_date)

            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            db.session.rollback()
            return f'There was an issue adding your task:{e}'

    return render_template('add_task.html')

# タスク完了切り替え（チェックボックス切り替え）


@app.route('/toggle_complete/<int:id>', methods=['POST'])
@login_required
def toggle_complete(id):
    task = Task.query.get_or_404(id)
    task.completed = not task.completed
    try:
        db.session.commit()
        return redirect("/")
    except Exception as e:
        db.session.rollback()
        return 'There was an issue adding your task'

# タスク削除


@app.route('/delete_task/<int:id>', methods=['POST'])
@login_required
def delete_task(id):
    task = Task.query.get_or_404(id)
    try:
        db.session.delete(task)
        db.session.commit()
        return redirect('/')
    except:
        db.session.rollback()
        return 'There was an issue adding your task'

# ログイン機能


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        next_url = request.args.get('next')
        
        try:
            # user = db.query(User).get(username)　主キー検索するために使う
            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password_hash, password):
                session['userid'] = user.id #セッションでidに関する情報も格納
                session['user'] = user.username
                flash(f"{username}でログインしました","success")
                return redirect(next_url or  url_for('index'))
            else:
                flash("ログインに失敗しました","error")
                return redirect(url_for('login'))
        except Exception as e:  # Exception as eでエラー内容を格納
            db.session.rollback()
            flash(f"ログイン処理でエラー:{e}", "error")
    return render_template('login.html')

# ユーザー登録機能


@app.route("/auth", methods=['POST', "GET"])
def auth():

    if request.method == 'POST':
        username = request.form.get('username','').strip()
        password = request.form.get('password','').strip()
        email = request.form.get('email','').strip()


        if not username or not password or not email:
            flash("ユーザー名，パスワード，emailは必須項目です","error")
            return redirect(url_for('auth'))

        #filter_byはor_などの条件文不可，filterは使用可能，first()で1件目を獲得
        dup = User.query.filter(or_(User.username==username, User.useremail==email)).first()

        if dup:
            if dup.username == username:
                flash("すでにこの名前のユーザーは存在します", 'error')
            elif dup.useremail == email:
                flash("すでにこのemailのユーザーは存在します", 'error')    

        else:
            try:
                    hashed_password = generate_password_hash(password)
                    new_user = User(username=username, password_hash=hashed_password,useremail=email)
                    db.session.add(new_user)
                    db.session.commit()
                    flash('ユーザー登録に成功しました', 'success')
                    return redirect(url_for('login'))
            except Exception as e:
                db.session.rollback()
                flash(f"ユーザー登録でエラーが起きました:{e}","error") #flashはflaskでメッセージ表示する機能
                return redirect(url_for('auth'))

    return render_template('auth.html')

# ログアウト機能


@app.route('/logout')
def logout():
    # session.pop('user', None)
    session.clear()
    flash("ログアウトしました", "success")
    return redirect('login')


if __name__ == "__main__":
    app.run(debug=True)
