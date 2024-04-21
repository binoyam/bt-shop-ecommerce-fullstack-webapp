from flask import Blueprint, jsonify, current_app
from flask_mysqldb import MySQL

remove_user_bp = Blueprint("remove_user", __name__)

mysql = MySQL()


# remove user and all orders by the user from db
@remove_user_bp.route("/api/remove_user/<int:user_id>", methods=["DELETE"])
def remove_user(user_id):
    try:
        # mysql.init_app(current_app)
        with mysql.connection.cursor() as cursor:

            cursor.execute("DELETE FROM orders_table WHERE user_id = %s", (user_id,))
            cursor.execute("DELETE FROM users_table WHERE id = %s", (user_id,))
            mysql.connection.commit()
            response_data = {"userRemoved": True}
        return jsonify(response_data), 200
    except Exception as e:
        print("Error removing user:", str(e))
        return jsonify({"userRemoved": False}), 500
