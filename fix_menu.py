import sqlite3

def fix_menu_schema():
    conn = sqlite3.connect("menu.db")
    cursor = conn.cursor()

    # Check current columns
    cursor.execute("PRAGMA table_info(menu)")
    columns = [col[1] for col in cursor.fetchall()]

    # Add price column if missing
    if "price" not in columns:
        cursor.execute("ALTER TABLE menu ADD COLUMN price REAL DEFAULT 0")
        print("✅ Added 'price' column to menu table.")
    else:
        print("ℹ️ 'price' column already exists.")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    fix_menu_schema()
