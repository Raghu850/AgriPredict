from flask import Flask, render_template, request, redirect, jsonify, url_for, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Function to connect to SQLite database
def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    role = data['role']

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ? AND role = ?', (username, role)).fetchone()
    conn.close()

    if user and check_password_hash(user['password'], password):
        session['username'] = username
        session['role'] = role
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Invalid credentials!'}), 401

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']
    role = data['role']

    hashed_password = generate_password_hash(password)

    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', (username, hashed_password, role))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except sqlite3.IntegrityError:
        return jsonify({'success': False, 'message': 'Username already exists!'}), 409

@app.route('/prediction')
def prediction():
    if 'username' in session:
        return render_template('prediction.html')
    else:
        return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
