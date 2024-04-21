from flask import Blueprint, jsonify
from flask_mysqldb import MySQL
from routes.helpers import convert_to_objects

users_bp = Blueprint("users", __name__)

mysql = MySQL()


@users_bp.route("/api/users")
def get_users():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users_table")
    users = convert_to_objects(cursor)
    cursor.close()
    return jsonify(users)
