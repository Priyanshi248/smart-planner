from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
from utils.ai_scheduler import recommend_time
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

app = Flask(__name__)

# 🔗 MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '_priyanshi24'
app.config['MYSQL_DB'] = 'smart_planner'

mysql = MySQL(app)


# 🏠 Home Page
@app.route('/')
def home():
    def home():
    tasks = []
    return render_template('index.html', tasks=tasks)


# 🔔 Reminder System (FIXED FOR 12-HOUR TIME)
def check_reminders():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tasks WHERE status='pending'")
    tasks = cur.fetchall()
    cur.close()

    now = datetime.now()

    for task in tasks:
        user_time = task[6]  # user selected time (e.g. 01:30 PM)

        if user_time:
            try:
                task_time = datetime.strptime(user_time, "%I:%M %p")

                # compare only time (ignore date)
                if abs((task_time.hour * 60 + task_time.minute) - (now.hour * 60 + now.minute)) <= 1:
                    print(f"🔔 Reminder: {task[1]}")

            except:
                pass


# ➕ Add Task
@app.route('/add_task', methods=['POST'])
def add_task():
    title = request.form['title']
    priority = request.form['priority']
    task_date = request.form.get('task_date') or None
    user_time = request.form.get('user_time') or None

    # 🤖 AI suggestion (already 12-hour)
    recommended = recommend_time(priority)

    # ✅ Prevent past dates
    if task_date:
        today = datetime.today().date()
        selected_date = datetime.strptime(task_date, "%Y-%m-%d").date()

        if selected_date < today:
            return "❌ Cannot select past date"

    cur = mysql.connection.cursor()
    cur.execute(
        """INSERT INTO tasks 
        (title, priority, status, recommended_time, task_date, user_time) 
        VALUES (%s, %s, %s, %s, %s, %s)""",
        (title, priority, "pending", recommended, task_date, user_time)
    )
    mysql.connection.commit()
    cur.close()

    return redirect('/')


# ✅ Complete Task
@app.route('/complete/<int:id>')
def complete_task(id):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE tasks SET status='completed' WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect('/')


# 🔄 Restore Task
@app.route('/restore/<int:id>')
def restore_task(id):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE tasks SET status='pending' WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect('/history')


# 📜 History Page
@app.route('/history')
def history():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tasks WHERE status='completed' ORDER BY task_date DESC")
    tasks = cur.fetchall()
    cur.close()

    grouped_tasks = {}

    for task in tasks:
        date = str(task[5]) if task[5] else "No Date"

        if date not in grouped_tasks:
            grouped_tasks[date] = []

        grouped_tasks[date].append(task)

    return render_template('history.html', grouped_tasks=grouped_tasks)


# 🗑 Delete Task
@app.route('/delete/<int:id>')
def delete_task(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM tasks WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()

    return redirect(request.referrer)


# ✏️ Edit Task Page
@app.route('/edit/<int:id>')
def edit_task(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tasks WHERE id=%s", (id,))
    task = cur.fetchone()
    cur.close()
    return render_template('edit.html', task=task)


# 💾 Update Task
@app.route('/update/<int:id>', methods=['POST'])
def update_task(id):
    title = request.form['title']
    priority = request.form['priority']
    task_date = request.form.get('task_date') or None
    user_time = request.form.get('user_time') or None

    # validate date again
    if task_date:
        today = datetime.today().date()
        selected_date = datetime.strptime(task_date, "%Y-%m-%d").date()

        if selected_date < today:
            return "❌ Cannot select past date"

    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE tasks 
        SET title=%s, priority=%s, task_date=%s, user_time=%s 
        WHERE id=%s
    """, (title, priority, task_date, user_time, id))

    mysql.connection.commit()
    cur.close()

    return redirect('/')


# ⏰ Background Scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(check_reminders, 'interval', seconds=30)
scheduler.start()


# 🚀 Run App
if __name__ == "__main__":
    app.run()
