from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(200), nullable=False)
    task_completed = db.Column(db.Boolean, default=False)
    task_date = db.Column(db.DateTime, default=datetime.utcnow)


@app.route('/', methods=["POST", "GET"])
def home():
    if request.method == "POST":
        task = request.form["input-task"]
        new_task = Todo(task_name=task)
        db.session.add(new_task)
        db.session.commit()
        return redirect("/")
    else:
        tasks = Todo.query.order_by(Todo.task_date).all()
        return render_template("index.html", todo_list = tasks)


@app.route('/delete/<int:id>')
def delete_task(id):
    task_to_delete = Todo.query.get(id)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect("/")

@app.route("/edit/<int:id>", methods=["POST", "GET"])
def edit_task(id):
    task_to_edit = Todo.query.get(id)
    if request.method == "POST":
        update_task = request.form["edit-input"]
        task_to_edit.task_name = update_task
        db.session.commit()

        return redirect("/")
    else:
        pass

    return render_template("edit.html", task=task_to_edit)


if __name__ == "__main__":
    app.run(debug=True)