import sqlite3

# Connect to the menu database
conn = sqlite3.connect("menu.db")
cursor = conn.cursor()

# Delete unwanted items
# NOTE: the menu table's column is called "item_name", not "item" -
# the previous version of this script referenced a column that
# doesn't exist and would raise sqlite3.OperationalError.
cursor.execute(
    "DELETE FROM menu WHERE item_name IN (?, ?, ?)",
    ("Paneer Butter Masala", "Dal Tadka", "Naan")
)

deleted = cursor.rowcount
conn.commit()
conn.close()

print(f"Removed {deleted} item(s) from the menu (Paneer Butter Masala, Dal Tadka, Naan).")
