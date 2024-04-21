from flask import Blueprint, jsonify, request
from flask_mysqldb import MySQL

feedback_bp = Blueprint("feedback", __name__)

mysql = MySQL()


# customer feedback form
@feedback_bp.route("/api/feedback", methods=["POST"])
def handle_contact_form():
    data = request.json
    print(data)
    name = data.get("name")
    email = data.get("email")
    message = data.get("message")

    cur = mysql.connection.cursor()

    cur.execute(
        "INSERT INTO feedback_table (name, email, message) VALUES (%s, %s, %s)",
        (name, email, message),
    )

    mysql.connection.commit()
    cur.close()
    response_data = {
        "feedbackSubmitted": "true",
    }
    return jsonify(response_data)
