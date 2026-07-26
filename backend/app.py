from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

# ---------------- USERS ----------------
def insert_user(name, email, phone_no):
    conn = sqlite3.connect('data.db')
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
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    conn.close()
    return jsonify(rows)

# ---------------- SEATS ----------------
def reset_seats():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    # Suppose you have 10 tables (1–10)
    for i in range(1, 11):
        cursor.execute("INSERT OR IGNORE INTO seats (table_no) VALUES (?)", (i,))
        cursor.execute("UPDATE seats SET status='unreserved' WHERE table_no=?", (i,))
    conn.commit()
    conn.close()

@app.route("/reset", methods=["POST"])
def reset():
    reset_seats()
    return jsonify({"message": "All seats reset to unreserved!"})

# ---------------- RESERVATIONS ----------------
def reserve_seat(table_no, name, time):
    conn = sqlite3.connect("data.db")
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
    else:
        conn.close()
        return {"error": f"Table {table_no} is already reserved!"}

@app.route("/reserve", methods=["POST"])
def reserve():
    data = request.get_json()
    table_no = data.get("table_no")
    name = data.get("name")
    time = data.get("time")

    result = reserve_seat(table_no, name, time)
    return jsonify(result)

@app.route("/vacant", methods=["GET"])
def vacant():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT table_no FROM seats WHERE status='unreserved'")
    rows = cursor.fetchall()
    conn.close()
    return jsonify([r[0] for r in rows])

@app.route("/reservations", methods=["GET"])
def get_reservations():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reservations")
    rows = cursor.fetchall()
    conn.close()
    return jsonify(rows)

# ---------------- HOME ----------------
@app.route("/")
def home():
    return "hello flask"

if __name__ == "__main__":
    app.run(debug=True)
