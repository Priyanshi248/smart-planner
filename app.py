from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from ai_scheduler import recommend_time
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime


app = Flask(__name__)
app.secret_key = "your_secret_key"

# 🔗 SQLite DB connection
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


# 🔧 Create table if not exists
def init_db():
    conn = get_db()

    # TASK TABLE
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    priority TEXT,
    status TEXT,
    recommended_time TEXT,
    task_date TEXT,
    user_time TEXT,
    user_id INTEGER
)
""")
    # USER TABLE ✅
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)

    conn.commit()
    conn.close()

init_db()   # 🔥 ADD HERE

@app.route('/login', methods=['GET','POST'])
def login():
    if 'user_id' in session:   # 🔥 ADD THIS
        return redirect('/')   # already logged in

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db()
        user = conn.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
        conn.close()

        if user and check_password_hash(user["password"], password):
            session['user_id'] = user["id"]
            return redirect('/')
        else:
            return "Invalid username or password"

    return render_template('login.html')

@app.route('/signup', methods=['GET','POST'])
def signup():
    if 'user_id' in session:   # 🔥 ADD THIS
        return redirect('/')

    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])

        conn = get_db()
        try:
            conn.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password)
            )
            conn.commit()
        except:
            return "Username already exists"
        finally:
            conn.close()

        return redirect('/login')

    return render_template('signup.html')

# 🏠 Home Page
@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect('/login')

    try:
        conn = get_db()
        tasks = conn.execute(
            "SELECT * FROM tasks WHERE status='pending' AND user_id=?",
            (session['user_id'],)
        ).fetchall()
        conn.close()
    except Exception as e:
        return f"Error: {str(e)}"   # 🔥 THIS WILL SHOW REAL ERROR

    return render_template('index.html', tasks=tasks)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/login')


# 🔔 Reminder System
def check_reminders():
    conn = get_db()
    tasks = conn.execute("SELECT * FROM tasks WHERE user_id=?").fetchall()
    conn.close()

    now = datetime.now()

    for task in tasks:
        user_time = task["user_time"]

        if user_time:
            try:
                task_time = datetime.strptime(user_time, "%H:%M")

                if abs((task_time.hour * 60 + task_time.minute) - (now.hour * 60 + now.minute)) <= 1:
                    print(f"🔔 Reminder: {task['title']}")

            except:
                pass


# ➕ Add Task
@app.route('/add_task', methods=['POST'])
def add_task():
    if 'user_id' not in session:   # 🔥 ADD THIS
        return redirect('/login')
    title = request.form['title']
    priority = request.form['priority']
    task_date = request.form.get('task_date') or None
    user_time = request.form.get('user_time') or None

    recommended = recommend_time(priority)

    # ✅ Prevent past dates
    if task_date:
        today = datetime.today().date()
        selected_date = datetime.strptime(task_date, "%Y-%m-%d").date()

        if selected_date < today:
            return "❌ Cannot select past date"

    conn = get_db()
    conn.execute(
        "INSERT INTO tasks (title, priority, status, recommended_time, task_date, user_time, user_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (title, priority, "pending", recommended, task_date, user_time, session['user_id'])
)
    conn.commit()
    conn.close()

    return redirect('/')


# ✅ Complete Task
@app.route('/complete/<int:id>')
def complete_task(id):
    if 'user_id' not in session:
        return redirect('/login')
    conn = get_db()
    conn.execute(
    "UPDATE tasks SET status='completed' WHERE id=? AND user_id=?",
    (id, session['user_id'])
)
    conn.commit()
    conn.close()
    return redirect('/')


# 🔄 Restore Task
@app.route('/restore/<int:id>')
def restore_task(id):
    if 'user_id' not in session:
        return redirect('/login')
    conn = get_db()
    conn.execute(
    "UPDATE tasks SET status='pending' WHERE id=? AND user_id=?",
    (id, session['user_id'])
)
    conn.commit()
    conn.close()
    return redirect('/history')


# 📜 History Page
@app.route('/history')
def history():
    if 'user_id' not in session:
        return redirect('/login')
    conn = get_db()
    tasks = conn.execute(
    "SELECT * FROM tasks WHERE status='completed' AND user_id=? ORDER BY task_date DESC",
    (session['user_id'],)
).fetchall()
    conn.close()

    grouped_tasks = {}

    for task in tasks:
        date = str(task["task_date"]) if task["task_date"] else "No Date"

        if date not in grouped_tasks:
            grouped_tasks[date] = []

        grouped_tasks[date].append(task)

    return render_template('history.html', grouped_tasks=grouped_tasks)


# 🗑 Delete Task
@app.route('/delete/<int:id>')
def delete_task(id):
    if 'user_id' not in session:
        return redirect('/login')
    conn = get_db()
    conn.execute(
    "DELETE FROM tasks WHERE id=? AND user_id=?",
    (id, session['user_id'])
)
    conn.commit()
    conn.close()

    return redirect(request.referrer)


# ✏️ Edit Task Page
@app.route('/edit/<int:id>')
def edit_task(id):
    if 'user_id' not in session:
        return redirect('/login')
    conn = get_db()
    task = conn.execute(
    "SELECT * FROM tasks WHERE id=? AND user_id=?",
    (id, session['user_id'])
).fetchone()
    conn.close()
    return render_template('edit.html', task=task)


# 💾 Update Task
@app.route('/update/<int:id>', methods=['POST'])
def update_task(id):
    if 'user_id' not in session:
        return redirect('/login')
    title = request.form['title']
    priority = request.form['priority']
    task_date = request.form.get('task_date') or None
    user_time = request.form.get('user_time') or None

    if task_date:
        today = datetime.today().date()
        selected_date = datetime.strptime(task_date, "%Y-%m-%d").date()

        if selected_date < today:
            return "Cannot select past date"

    conn = get_db()
    conn.execute("""
    UPDATE tasks 
    SET title=?, priority=?, task_date=?, user_time=? 
    WHERE id=? AND user_id=?
""", (title, priority, task_date, user_time, id, session['user_id']))

    conn.commit()
    conn.close()

    return redirect('/')


# ⏰ Background Scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(check_reminders, 'interval', seconds=30)

if __name__ == "__main__":
    scheduler.start()
    app.run(debug=True)
