
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# In-memory database
users = {}

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Backend is running"})


@app.route("/register", methods=["POST"])
def register():
    data = request.json

    username = data.get("username")
    password = data.get("password")

    if not username:
        return jsonify({"error": "Username is required"}), 400

    # ❗❗❗ Intentional Bug ❗❗❗
    # PRD要求：用户名长度必须 > 6
    # 这里故意不校验

    if not password:
        return jsonify({"error": "Password is required"}), 400

    if len(password) <= 6:
        return jsonify({"error": "Password must be longer than 6 characters"}), 400

    if username in users:
        return jsonify({"error": "Username already exists"}), 400

    users[username] = password

    return jsonify({"message": "Register success"}), 200


@app.route("/login", methods=["POST"])
def login():
    data = request.json

    username = data.get("username")
    password = data.get("password")

    if not username:
        return jsonify({"error": "Username is required"}), 400

    if not password:
        return jsonify({"error": "Password is required"}), 400

    if username not in users:
        return jsonify({"error": "User does not exist"}), 400

    if users[username] != password:
        return jsonify({"error": "Incorrect password"}), 400

    return jsonify({
        "message": "Login success",
        "data": "Welcome! You have successfully logged in."
    }), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)
