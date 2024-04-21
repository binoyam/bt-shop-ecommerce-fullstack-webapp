from flask import Blueprint, jsonify, request
from flask_mysqldb import MySQL

auth_bp = Blueprint("auth", __name__)

mysql = MySQL()


@auth_bp.route("/api/login", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    cursor = mysql.connection.cursor()
    cursor.execute(
        "SELECT * FROM users_table WHERE name = %s AND password = %s",
        (username, password),
    )
    account = cursor.fetchone()

    if account:
        customer_id = account[0]
        customer_name = account[1]
        customer_email = account[2]
        is_admin = account[6]

        if is_admin:
            response_data = {
                "loginSuccess": "true",
                "customerId": customer_id,
                "customerName": customer_name,
                "customerEmail": customer_email,
                "isAdmin": True,
            }
        else:
            response_data = {
                "loginSuccess": "true",
                "customerId": customer_id,
                "customerName": customer_name,
                "customerEmail": customer_email,
                "isAdmin": False,
            }

    else:
        response_data = {"loginSuccess": "false"}

    return jsonify(response_data)


# signup new user
@auth_bp.route("/api/signup", methods=["POST"])
def signup():
    signup_data = request.json
    cursor = mysql.connection.cursor()
    cursor.execute(
        "SELECT * FROM users_table WHERE email = %s", (signup_data["email"],)
    )
    existing_user = cursor.fetchone()
    if existing_user:
        response_data = {
            "signupSuccess": "false1",
            "message": "Email already registered",
        }
    else:
        query = "INSERT INTO users_table (name, email, password, gender, phoneNumber) VALUES (%s, %s, %s, %s, %s)"
        values = (
            signup_data["username"],
            signup_data["email"],
            signup_data["password"],
            signup_data["gender"],
            signup_data["phoneNumber"],
        )
        cursor.execute(query, values)
        mysql.connection.commit()
        cursor.execute(
            "SELECT * FROM users_table WHERE name = %s AND password = %s",
            (signup_data["username"], signup_data["password"]),
        )
        account = cursor.fetchone()
        if account:
            customer_id = account[0]
            customer_name = account[1]
            customer_email = account[2]
            response_data = {
                "signupSuccess": "true",
                "customerId": customer_id,
                "customerName": customer_name,
                "customerEmail": customer_email,
            }

        else:
            response_data = {"signupSuccess": "false"}
    cursor.close()

    return jsonify(response_data)
