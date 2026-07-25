from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

def insert_user(name, email, phone_no):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (name, email, phone_no) VALUES (?, ?, ?)',
                   (name, email, phone_no))
    conn.commit()
    conn.close()

@app.route("/")
def home():
    return "hello flask"

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


if __name__ == "__main__":
    app.run(debug=True)
