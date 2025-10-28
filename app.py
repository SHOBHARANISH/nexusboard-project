from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/project_head', methods=['GET', 'POST'])
def project_head():
    error = None
    if request.method == 'POST':
        password = request.form['password']
        if password == 'Bright2026!':
            return render_template('dashboard.html')
        else:
            error = "Incorrect Password"
    return render_template('password.html', error=error)


# Existing routes for frontend, backend, database remain unchanged
@app.route('/frontend')
def frontend():
    return render_template('frontend.html')

@app.route('/backend')
def backend():
    return render_template('backend.html')

@app.route('/database')
def database():
    return render_template('database.html')

if __name__ == "__main__":
    app.run(debug=True)
