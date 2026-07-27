import sqlite3

def seed_menu():
    conn = sqlite3.connect('menu.db')
    cursor = conn.cursor()

    # Menu items with total serves, remaining serves, and price
    dishes = [
        ("Cheese Pizza", 0, 50, 299),
        ("Veg Burger", 0, 70, 249),
        ("White Sauce Pasta", 0, 50, 349),
        ("Cold Coffee", 0, 50, 149),
        ("Fresh Salad", 0, 50, 199),
        ("Chocolate Cake", 0, 50, 229)
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
