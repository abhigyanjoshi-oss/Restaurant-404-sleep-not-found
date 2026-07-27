import sqlite3

# Connect to your menu database
conn = sqlite3.connect("menu.db")
cursor = conn.cursor()

# Delete unwanted items
cursor.execute("DELETE FROM menu WHERE item IN ('Paneer Butter Masala', 'Dal Tadka', 'Naan');")

# Save changes and close
conn.commit()
conn.close()

print("Items removed successfully!")
