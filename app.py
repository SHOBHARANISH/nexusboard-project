from flask import Flask, render_template, request, redirect, url_for, session, flash
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# ---------------- DATABASE CONFIGURATION -----------------
db_config = {
    'host': 'localhost',
    'database': 'demo2',
    'user': 'postgres',
    'password': 'shobha'
}

def get_db_connection():
    return psycopg2.connect(**db_config)

def create_users_table():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

def create_tasks_table():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            assigned_to VARCHAR(100) NOT NULL,
            task_type VARCHAR(50) NOT NULL,
            duration VARCHAR(50) NOT NULL
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

create_users_table()
create_tasks_table()

# ---------------- AUTH ROUTES -----------------
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('home_page'))
    return redirect(url_for('login'))

@app.route('/index')
def index_page():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        hashed_pw = generate_password_hash(password)

        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                        (name, email, hashed_pw))
            conn.commit()
            flash("✅ Registration successful! Please log in.", "success")
            return redirect(url_for('login'))
        except psycopg2.IntegrityError:
            conn.rollback()
            flash("⚠️ Email already exists.", "danger")
        finally:
            cur.close()
            conn.close()
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name, email, password FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user and check_password_hash(user[3], password):
            session['user_id'] = user[0]
            session['user_name'] = user[1]
            flash("🎉 Login successful!", "success")
            return redirect(url_for('home_page'))
        else:
            flash("❌ Invalid email or password.", "danger")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("👋 You have been logged out.", "info")
    return redirect(url_for('login'))

# ---------------- MAIN PAGES -----------------
@app.route('/home')
def home_page():
    if 'user_id' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('login'))
    return render_template('home.html', name=session['user_name'])

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('login'))
    user = {
        'name': 'Ram',
        'bio': 'MCA Student',
        'email': 'ram@example.com',
        'phone': '+91 9876543210',
        'branch': 'Computer Applications',
        'project_name': 'NotifyNet Dashboard System',
        'project_status': 'In Progress',
        'project_goal': 'Create a smart college communication platform',
        'next_project': 'AI-powered Attendance Tracker'
    }
    return render_template('profile.html', user=user)

@app.route('/update_profile')
def update_profile():
    return "<h3>Update Profile Page (Coming Soon)</h3>"

# ---------------- PROJECT HEAD -----------------
@app.route('/project_head', methods=['GET', 'POST'])
def project_head():
    if 'user_id' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('login'))

    if 'project_head_authenticated' not in session:
        session['project_head_authenticated'] = False

    error = None
    if not session['project_head_authenticated']:
        if request.method == 'POST' and 'password' in request.form:
            password = request.form['password']
            if password == '123':  # project head password
                session['project_head_authenticated'] = True
                flash("✅ Access granted! Welcome Project Head.", "success")
                return redirect(url_for('project_head'))
            else:
                error = "❌ Incorrect password"
        return render_template('password.html', error=error)

    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == 'POST' and 'title' in request.form:
        task_id = request.form.get('task_id')
        title = request.form['title']
        assigned_to = request.form['assigned_to']
        task_type = request.form['task_type']
        duration = request.form['duration']

        if task_id:
            cur.execute("UPDATE tasks SET title=%s, assigned_to=%s, task_type=%s, duration=%s WHERE id=%s",
                        (title, assigned_to, task_type, duration, task_id))
            flash("✏️ Task updated successfully!", "success")
        else:
            cur.execute("INSERT INTO tasks (title, assigned_to, task_type, duration) VALUES (%s,%s,%s,%s)",
                        (title, assigned_to, task_type, duration))
            flash("✅ Task created successfully!", "success")
        conn.commit()

    cur.execute("SELECT * FROM tasks ORDER BY id DESC")
    tasks = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('project_head.html', tasks=tasks)

@app.route('/delete_task/<int:task_id>')
def delete_task(task_id):
    if 'user_id' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('login'))

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id=%s", (task_id,))
    conn.commit()
    cur.close()
    conn.close()
    flash("Task deleted successfully!", "success")
    return redirect(url_for('project_head'))

# ---------------- FRONTEND / BACKEND / DATABASE -----------------
@app.route('/frontend')
def frontend():
    if 'user_id' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('login'))
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, title, assigned_to, duration FROM tasks WHERE task_type='frontend'")
    tasks = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('frontend.html', tasks=tasks)

@app.route('/backend')
def backend():
    if 'user_id' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('login'))
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, title, assigned_to, duration FROM tasks WHERE task_type='backend'")
    tasks = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('backend.html', tasks=tasks)

@app.route('/database')
def database():
    if 'user_id' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('login'))
    conn = get_db_connection()
    cur = conn.cursor()
    # Fetch only database tasks
    cur.execute("SELECT id, title, assigned_to, duration FROM tasks WHERE task_type='database'")
    tasks = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('database.html', tasks=tasks)

# ---------------- RUN APP -----------------
if __name__ == '__main__':
    app.run(debug=True)
