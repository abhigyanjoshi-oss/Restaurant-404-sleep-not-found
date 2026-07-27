import os
import sqlite3
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# ---------------- DB PATHS ----------------
# Use absolute paths anchored to the project root (one level above this
# file). Previously the code used bare "data.db" / "menu.db" strings,
# which resolve relative to whatever directory the process happens to
# be launched from. Running `python backend/app.py` from the project
# root vs `python app.py` from inside backend/ silently created two
# *different* database files, which is why the front end and back end
# could drift out of sync (e.g. removed menu items reappearing).
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
DATA_DB = os.path.join(PROJECT_ROOT, "data.db")
MENU_DB = os.path.join(PROJECT_ROOT, "menu.db")


def get_data_conn():
    return sqlite3.connect(DATA_DB)


def get_menu_conn():
    return sqlite3.connect(MENU_DB)


# ---------------- USERS ----------------
def insert_user(name, email, phone_no):
    conn = get_data_conn()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (name, email, phone_no) VALUES (?, ?, ?)',
                   (name, email, phone_no))
    conn.commit()
    conn.close()

@app.route("/login", methods=["POST"])
def user_details():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    phone_no = data.get("phone_no")

    insert_user(name, email, phone_no)
    return jsonify({"message": "User stored successfully!"})

@app.route("/users", methods=["GET"])
def get_users():
    conn = get_data_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    conn.close()
    return jsonify([{"id": r[0], "name": r[1], "email": r[2], "phone_no": r[3]} for r in rows])

# ---------------- SEATS ----------------
def reset_seats():
    conn = get_data_conn()
    cursor = conn.cursor()
    for i in range(1, 7):  # 6 tables (matches seed_seats.py / the UI)
        cursor.execute("INSERT OR IGNORE INTO seats (table_no) VALUES (?)", (i,))
        cursor.execute("UPDATE seats SET status='unreserved' WHERE table_no=?", (i,))
    conn.commit()
    conn.close()

@app.route("/reset", methods=["POST"])
def reset():
    reset_seats()
    return jsonify({"message": "All seats reset to unreserved!"})

@app.route("/tables", methods=["GET"])
def get_tables():
    conn = get_data_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT table_no, status FROM seats ORDER BY table_no")
    rows = cursor.fetchall()
    conn.close()
    return jsonify([{"table_no": r[0], "status": r[1]} for r in rows])

# ---------------- RESERVATIONS ----------------
def reserve_seat(table_no, name, time):
    conn = get_data_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM seats WHERE table_no=?", (table_no,))
    result = cursor.fetchone()

    if result and result[0] == "unreserved":
        cursor.execute("UPDATE seats SET status='reserved' WHERE table_no=?", (table_no,))
        cursor.execute("INSERT INTO reservations (table_no, name, time) VALUES (?, ?, ?)",
                       (table_no, name, time))
        conn.commit()
        conn.close()
        return {"message": f"Table {table_no} reserved for {name} at {time}"}
    elif result:
        conn.close()
        return {"error": f"Table {table_no} is already reserved!"}
    else:
        conn.close()
        return {"error": f"Table {table_no} does not exist!"}

@app.route("/reserve", methods=["POST"])
def reserve():
    data = request.get_json()
    table_no = data.get("table_no")
    name = data.get("name")
    time = data.get("time")
    result = reserve_seat(table_no, name, time)
    status_code = 200 if "message" in result else 400
    return jsonify(result), status_code

@app.route("/vacant", methods=["GET"])
def vacant():
    conn = get_data_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT table_no FROM seats WHERE status='unreserved'")
    rows = cursor.fetchall()
    conn.close()
    return jsonify([r[0] for r in rows])

@app.route("/reservations", methods=["GET"])
def get_reservations():
    conn = get_data_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reservations")
    rows = cursor.fetchall()
    conn.close()
    return jsonify([{"id": r[0], "table_no": r[1], "name": r[2], "time": r[3]} for r in rows])

# ---------------- MENU ----------------
def reset_menu():
    conn = get_menu_conn()
    cursor = conn.cursor()
    cursor.execute("UPDATE menu SET remaining_serves = total_serves")
    conn.commit()
    conn.close()

@app.route('/reset_menu', methods=['POST'])
def reset_menu_route():
    reset_menu()
    return jsonify({"message": "Menu reset for the day"})

@app.route('/menu', methods=['GET'])
def get_menu():
    conn = get_menu_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT item_name, remaining_serves, price FROM menu ORDER BY item_name")
    items = cursor.fetchall()
    conn.close()
    return jsonify([{"item": i[0], "remaining": i[1], "price": i[2]} for i in items])

@app.route('/order', methods=['POST'])
def place_order():
    data = request.get_json()
    table_no = data.get('table_no')
    item_name = data.get('item_name')

    conn1 = get_data_conn()
    cursor1 = conn1.cursor()
    cursor1.execute("SELECT status FROM seats WHERE table_no=?", (table_no,))
    seat = cursor1.fetchone()
    conn1.close()

    if not seat or seat[0] != 'reserved':
        return jsonify({"error": "Seat not reserved"}), 400

    conn2 = get_menu_conn()
    cursor2 = conn2.cursor()
    cursor2.execute("SELECT remaining_serves FROM menu WHERE item_name=?", (item_name,))
    result = cursor2.fetchone()

    if result and result[0] > 0:
        cursor2.execute("UPDATE menu SET remaining_serves = remaining_serves - 1 WHERE item_name=?", (item_name,))
        conn2.commit()
        conn2.close()
        return jsonify({"message": f"{item_name} served to table {table_no}"})
    elif result:
        conn2.close()
        return jsonify({"error": f"{item_name} is sold out"}), 400
    else:
        conn2.close()
        return jsonify({"error": f"{item_name} is not on the menu"}), 404

# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
