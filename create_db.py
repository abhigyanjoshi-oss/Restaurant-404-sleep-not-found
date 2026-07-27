import sqlite3

# Create database and tables
conn = sqlite3.connect('data.db')
cursor = conn.cursor()

# Users table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        phone_no TEXT
    )
''')

# Reservations table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS reservations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        table_no INTEGER NOT NULL,
        name TEXT NOT NULL,
        time TEXT NOT NULL
    )
''')

# Seats table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS seats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        table_no INTEGER UNIQUE NOT NULL,
        status TEXT DEFAULT 'unreserved'
    )
''')

conn.commit()
conn.close()
print("Database created successfully!")
