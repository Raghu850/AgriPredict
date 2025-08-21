import sqlite3
from werkzeug.security import generate_password_hash

# Connect to DB
conn = sqlite3.connect("user_admin_login.db")
cursor = conn.cursor()

# Create admin
username = "admin"
password = "123456"
hashed_password = generate_password_hash(password)

cursor.execute("""
INSERT INTO users (username, password)
VALUES (?, ?)
""", (username, hashed_password))

conn.commit()
conn.close()

print("✅ Admin user added successfully!")
