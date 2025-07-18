import sqlite3

def view_users():
    conn = sqlite3.connect('user_admin_login.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()

    print("Users:")
    for user in users:
        print(f"ID: {user[0]}, Username: {user[1]}")

    conn.close()

def view_admins():
    conn = sqlite3.connect('user_admin_login.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM admins')
    admins = cursor.fetchall()

    print("\nAdmins:")
    for admin in admins:
        print(f"ID: {admin[0]}, Username: {admin[1]}")

    conn.close()

if __name__ == '__main__':
    view_users()
    view_admins()
