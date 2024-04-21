from flask import Blueprint, jsonify
from flask_mysqldb import MySQL

get_products_bp = Blueprint("get_products", __name__)

mysql = MySQL()


@get_products_bp.route("/api/products", methods=["GET"])
def get_products():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM products_table")
    columns = [column[0] for column in cursor.description]
    products = []
    for row in cursor.fetchall():
        product = {}
        for i, column in enumerate(columns):
            product[column] = row[i]
        products.append(product)
    cursor.close()
    # print(products)
    return jsonify(products)
