import sqlite3

def seed_menu():
    conn = sqlite3.connect('menu.db')
    cursor = conn.cursor()

    # Menu items with total serves, remaining serves, and price
    dishes = [
        ("Cheese Pizza", 10, 10, 250),
        ("Veg Burger", 15, 15, 150),
        ("White Sauce Pasta", 12, 12, 200),
        ("Cold Coffee", 20, 20, 100),
        ("Fresh Salad", 15, 15, 120),
        ("Chocolate Cake", 8, 8, 180)
    ]

    # Insert all dishes
    for dish in dishes:
        cursor.execute(
            "INSERT OR REPLACE INTO menu (item_name, total_serves, remaining_serves, price) VALUES (?, ?, ?, ?)",
            dish
        )

    # Commit once after all inserts
    conn.commit()
    conn.close()
    print("Menu seeded successfully!")

if __name__ == "__main__":
    seed_menu()
