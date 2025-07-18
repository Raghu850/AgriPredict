from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key

# Database connection
def get_db_connection():
    conn = sqlite3.connect('user_admin_login.db')
    conn.row_factory = sqlite3.Row  # Enable column access by name
    return conn

# Create login, admin, and reviews tables
def create_login_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            rating INTEGER NOT NULL,
            content TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

# Home Route
@app.route('/')
def index():
    return render_template('home.html')

# Login Route for both users and admins
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        conn = get_db_connection()

        if role == 'user':
            user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
            if user is None:
                flash('Account not found!', 'error')
            elif check_password_hash(user['password'], password):
                session['username'] = username
                flash('User login successful!', 'success')
                return redirect(url_for('prediction'))
            else:
                flash('Incorrect password!', 'error')

        elif role == 'admin':
            admin = conn.execute('SELECT * FROM admins WHERE username = ?', (username,)).fetchone()
            if admin is None:
                flash('Account not found!', 'error')
            elif check_password_hash(admin['password'], password):
                session['admin_username'] = username
                flash('Admin login successful!', 'success')
                return redirect(url_for('admin_dashboard'))
            else:
                flash('Incorrect password!', 'error')

        conn.close()

    return render_template('login.html')

# Registration Route for users
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
            conn.commit()
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists! Please choose a different username.', 'error')
        finally:
            conn.close()

    return render_template('register.html')

# Prediction Route (accessible to logged-in users)
@app.route('/prediction', methods=['GET', 'POST'])
def prediction():
    if 'username' not in session:
        flash('You need to log in first!', 'error')
        return redirect(url_for('login'))

    if request.method == 'POST':
        year = request.form['year']
        temperature = request.form['temperature']
        rainfall = request.form['rainfall']
        humidity = request.form['humidity']
        supply_indicator = request.form['supply_indicator']
        demand_indicator = request.form['demand_indicator']
        crop_type = request.form['crop_type']

        # Example prediction logic (you can replace this with your model)
        predicted_price = 5000  # Replace with actual prediction logic
        predicted_category = "High" if predicted_price > 3000 else "Low"

        return render_template('prediction.html', predicted_price=predicted_price, predicted_category=predicted_category)

    return render_template('prediction.html')

# Admin Dashboard to view all reviews
@app.route('/admin_dashboard')
def admin_dashboard():
    if 'admin_username' not in session:
        flash('You need to log in as an admin first!', 'error')
        return redirect(url_for('login'))

    conn = get_db_connection()
    reviews = conn.execute('SELECT * FROM reviews ORDER BY id DESC').fetchall()
    conn.close()

    return render_template('admin_dashboard.html', reviews=reviews)

# Reviews Route
@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
    if request.method == 'POST':
        name = request.form['name']
        rating = request.form['rating']
        review_content = request.form['review']

        conn = get_db_connection()
        conn.execute('INSERT INTO reviews (name, rating, content) VALUES (?, ?, ?)', (name, rating, review_content))
        conn.commit()
        conn.close()
        flash('Thank you for your review!', 'success')
        return redirect(url_for('reviews'))

    conn = get_db_connection()
    reviews = conn.execute('SELECT * FROM reviews ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('reviews.html', reviews=reviews)

# Logout Route
@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('admin_username', None)
    flash('You have been logged out!', 'success')
    return redirect(url_for('login'))

# Initialize the database and run the app
if __name__ == '__main__':
    create_login_tables()  # Ensure the tables are created
    app.run(debug=True)
