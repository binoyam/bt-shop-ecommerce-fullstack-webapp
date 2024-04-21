from flask import Blueprint, jsonify, logging
from flask_mysqldb import MySQL

remove_order_bp = Blueprint("remove_order", __name__)

mysql = MySQL()

# remove order from table 
@remove_order_bp.route("/api/orders/<int:order_id>", methods=["DELETE"])
def remove_order(order_id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM orders_table WHERE id = %s", (order_id,))
        mysql.connection.commit()

        cursor.close()
        response_data = {"orderRemoved": True}
        return jsonify(response_data), 200
    except Exception as e:
        error_message = "An error occured while removing the order."
        logging.error(f"{error_message} Error Details: {str(e)}")
        return jsonify({"error": error_message}), 500
