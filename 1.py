import sqlite3
from werkzeug.security import generate_password_hash

# Connect to DB
conn = sqlite3.connect("user_admin_login.db")
cursor = conn.cursor()

# New admin credentials
username = "admin"
password = "123456"
hashed_password = generate_password_hash(password)

# Insert into admins table
cursor.execute("""
INSERT INTO admins (username, password)
VALUES (?, ?)
""", (username, hashed_password))

conn.commit()
conn.close()

print("✅ New admin added successfully!")
