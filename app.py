
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "todo_secret_key"

DB_NAME = "todo.db"


def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL
            )
        """)
        conn.commit()

init_db()


@app.route('/')
def index():

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM tasks ORDER BY id DESC")
        tasks = cursor.fetchall()

        print("\n========== DATABASE ==========")
        print(f"Total Tasks: {len(tasks)}")

        for task_id, task_name in tasks:
            print(f"ID: {task_id} | Task: {task_name}")

        print("==============================\n")

    return render_template("index.html", tasks=tasks)


@app.route('/add', methods=['POST'])
def add():
    task = request.form['task']

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tasks(task) VALUES(?)",
            (task,)
        )
        conn.commit()

    flash("✅ Task added successfully!", "success")
    return redirect(url_for('index'))


@app.route('/update/<int:task_id>', methods=['POST'])
def update(task_id):
    new_task = request.form['new-task']

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE tasks SET task=? WHERE id=?",
            (new_task, task_id)
        )
        conn.commit()

    flash("♾️ Task updated successfully!", "info")
    return redirect(url_for('index'))


@app.route('/delete/<int:task_id>')
def delete(task_id):

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM tasks WHERE id=?",
            (task_id,)
        )
        conn.commit()

    flash("🗑️ Task deleted successfully!", "danger")
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
