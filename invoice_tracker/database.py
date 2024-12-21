import sqlite3

def init_db():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    
    # Create table for electronics inventory
    c.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            category TEXT NOT NULL,
            sector TEXT NOT NULL,
            application TEXT NOT NULL,
            date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
