import os, sqlite3
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "studyflow-local-secret")
DB_PATH = os.getenv("STUDYNEST_DB", os.path.join(os.path.dirname(__file__), "studyflow.db"))

def connect():
    c = sqlite3.connect(DB_PATH)
    c.row_factory = sqlite3.Row
    return c

def init_db():
    with connect() as c:
        c.execute("""CREATE TABLE IF NOT EXISTS tasks(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL, subject TEXT NOT NULL, due_date TEXT NOT NULL DEFAULT '',
            priority TEXT NOT NULL DEFAULT 'Medium', done INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL)""")
        if c.execute("SELECT COUNT(*) FROM tasks").fetchone()[0] == 0:
            demo = [
                ("Review sorting algorithms", "Data Structures", "2026-10-22", "High", 0),
                ("Finish cloud computing notes", "Cloud Computing", "2026-10-23", "Medium", 0),
                ("Practice SQL joins", "Database Systems", "2026-10-24", "Medium", 1),
                ("Revise operating systems", "Operating Systems", "2026-10-25", "Low", 0),
            ]
            c.executemany("INSERT INTO tasks(title,subject,due_date,priority,done,created_at) VALUES(?,?,?,?,?,?)",
                          [(*t, datetime.now().strftime("%Y-%m-%d %H:%M")) for t in demo])

@app.route("/")
def home():
    q = request.args.get("q", "").strip()
    with connect() as c:
        if q:
            tasks = c.execute("SELECT * FROM tasks WHERE title LIKE ? OR subject LIKE ? ORDER BY done, due_date",
                              (f"%{q}%", f"%{q}%")).fetchall()
        else:
            tasks = c.execute("SELECT * FROM tasks ORDER BY done, due_date, id DESC").fetchall()
        all_tasks = c.execute("SELECT * FROM tasks").fetchall()
    stats = {"total": len(all_tasks), "done": sum(t["done"] for t in all_tasks),
             "pending": sum(not t["done"] for t in all_tasks),
             "high": sum(t["priority"] == "High" and not t["done"] for t in all_tasks)}
    return render_template("index.html", tasks=tasks, stats=stats, q=q)

@app.route("/tasks/add", methods=["POST"])
def add_task():
    title = request.form.get("title", "").strip()
    subject = request.form.get("subject", "").strip()
    due_date = request.form.get("due_date", "").strip()
    priority = request.form.get("priority", "Medium")
    if not title or not subject:
        flash("Add a task name and subject.", "error")
    elif priority not in ["High", "Medium", "Low"]:
        flash("Choose a valid priority.", "error")
    else:
        with connect() as c:
            c.execute("INSERT INTO tasks(title,subject,due_date,priority,done,created_at) VALUES(?,?,?,?,0,?)",
                      (title, subject, due_date, priority, datetime.now().strftime("%Y-%m-%d %H:%M")))
        flash("Task added to your plan.", "success")
    return redirect(url_for("home"))

@app.route("/tasks/<int:task_id>/toggle", methods=["POST"])
def toggle_task(task_id):
    with connect() as c:
        c.execute("UPDATE tasks SET done = CASE done WHEN 1 THEN 0 ELSE 1 END WHERE id = ?", (task_id,))
    return redirect(url_for("home"))

@app.route("/tasks/<int:task_id>/delete", methods=["POST"])
def delete_task(task_id):
    with connect() as c:
        c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    flash("Task removed.", "success")
    return redirect(url_for("home"))

@app.route("/api/tasks")
def api_tasks():
    with connect() as c:
        rows = c.execute("SELECT * FROM tasks ORDER BY id DESC").fetchall()
    return jsonify([dict(row) for row in rows])

@app.route("/health")
def health():
    return jsonify(status="healthy", app="StudyFlow")

init_db()
if __name__ == "__main__":
    app.run(debug=True, port=int(os.getenv("PORT", "5000")))
