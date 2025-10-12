from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import date

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    completed = db.Column(db.Boolean, default=False)


@app.route("/")
def index():
    tasks = Task.query.all()
    return render_template("index.html", tasks=tasks)


@app.route('/add_task', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        content = request.form.get('content')
        due_date_str = request.form.get('due_date')

        try:
            due_date = date.fromisoformat(due_date_str)
            new_task = Task(content=content, due_date=due_date)

            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except:
            db.session.rollback()
            return 'There was an issue adding your task'

    return render_template('add_task.html')


@app.route('/toggle_complete/<int:id>', methods=['POST'])
def toggle_complete(id):
    task = Task.query.get_or_404(id)
    task.completed = not task.completed
    try:
        db.session.commit()
        return redirect("/")
    except:
        db.session.rollback()
        return 'There was an issue adding your task'


@app.route('/delete_task/<int:id>', methods=['POST'])
def delete_task(id):
    task = Task.query.get_or_404(id)
    try:
        db.session.delete(task)
        db.session.commit()
        return redirect('/')
    except:
        db.session.rollback()
        return 'There was an issue adding your task'


if __name__ == "__main__":
    app.run(debug=True)
