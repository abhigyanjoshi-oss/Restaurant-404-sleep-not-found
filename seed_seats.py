import sqlite3

def seed_seats():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # Seed 6 tables
    for i in range(1, 7):
        cursor.execute("INSERT OR IGNORE INTO seats (table_no, status) VALUES (?, 'unreserved')", (i,))

    conn.commit()
    conn.close()
    print("Seats seeded successfully!")

if __name__ == "__main__":
    seed_seats()
