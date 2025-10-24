from flask import Flask, render_template, request, redirect, url_for, session, flash
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
 

# Database Configuration
db_config = {
    'host': 'localhost',
    'database': 'demo',
    'user': 'postgres',
    'password': 'root'  # password
}

# Database Connection
def get_db_connection():
    conn = psycopg2.connect(**db_config)
    return conn


@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('home_page'))
    return redirect(url_for('login'))


# ---------------- REGISTER -----------------
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


# ---------------- LOGIN -----------------
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


# ---------------- HOME / LOGOUT -----------------
@app.route('/home')
def home_page():
    if 'user_id' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('login'))
    return render_template('home.html', name=session['user_name'])


@app.route('/logout')
def logout():
    session.clear()
    flash("👋 You have been logged out.", "info")
    return redirect(url_for('login'))


@app.route('/profile')
def profile():
    user = {
        'name': 'ram',
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


if __name__ == '__main__':
    app.run(debug=True)
