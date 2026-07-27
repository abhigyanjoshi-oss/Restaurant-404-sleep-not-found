import sqlite3

def create_menu_tables():
    conn = sqlite3.connect('menu.db')   # <-- new database file
    cursor = conn.cursor()

    # Menu table
    cursor.execute('''CREATE TABLE IF NOT EXISTS menu (
        item_name TEXT PRIMARY KEY,
        total_serves INTEGER NOT NULL,
        remaining_serves INTEGER NOT NULL,
        price REAL DEFAULT 0
    )''')

    conn.commit()
    conn.close()
    print("menu.db created successfully!")

if __name__ == "__main__":
    create_menu_tables()
