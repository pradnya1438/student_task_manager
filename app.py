from flask import Flask, request, jsonify
from flask_cors import CORS
from db import get_db_connection

app = Flask(__name__)
CORS(app)

# ---------- AUTH ----------

@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
        (data["name"], data["email"], data["password"])
    )
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Signup successful"})


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT id FROM users WHERE email=%s AND password=%s",
        (data["email"], data["password"])
    )
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user:
        return jsonify({"user_id": user["id"]})
    return jsonify({"message": "Invalid login"}), 401
@app.route("/add-task", methods=["POST"])
def add_task():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO tasks (user_id, task) VALUES (%s, %s)",
        (data["user_id"], data["task"])
    )
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Task added"})


@app.route("/tasks/<int:user_id>")
def get_tasks(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM tasks WHERE user_id=%s", (user_id,))
    tasks = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(tasks)


@app.route("/complete-task/<int:task_id>", methods=["PUT"])
def complete_task(task_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE tasks SET completed=TRUE WHERE id=%s",
        (task_id,)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Task completed"})
@app.route("/delete-task/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tasks WHERE id=%s", (task_id,))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": "Task deleted"})


if __name__ == "__main__":
    app.run(debug=True)