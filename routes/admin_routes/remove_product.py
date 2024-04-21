from flask import Blueprint, jsonify
from flask_mysqldb import MySQL

remove_product_bp = Blueprint("remove_product", __name__)

mysql = MySQL()


@remove_product_bp.route("/api/remove_product/<int:product_id>", methods=["DELETE"])
def remove_product(product_id):
    try:
        with mysql.connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM orders_table WHERE product_id = %s", (product_id,)
            )
            cursor.execute("DELETE FROM products_table WHERE id = %s", (product_id,))
            mysql.connection.commit()

            cursor.close()
        return jsonify({"productRemoved": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
