from flask import Blueprint, jsonify
from flask_mysqldb import MySQL
from routes.helpers import convert_to_objects

products_bp = Blueprint("products", __name__)

mysql = MySQL()


@products_bp.route("/api/all_products")
def get_all_products():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM products_table")
    products = convert_to_objects(cursor)
    cursor.close()
    return jsonify(products)
