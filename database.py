import sqlite3

def init_db():
    conn = sqlite3.connect('crop_profit.db')
    c = conn.cursor()
    
    # Create crop table
    c.execute('''CREATE TABLE IF NOT EXISTS crops (
                    id INTEGER PRIMARY KEY,
                    crop_name TEXT UNIQUE,
                    profit_per_acre REAL,
                    region TEXT)''')
    
    conn.commit()
    conn.close()

init_db()
