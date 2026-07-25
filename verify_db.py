import sqlite3

conn = sqlite3.connect('data.db')
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())  # Should show [('users',)]

conn.close()
