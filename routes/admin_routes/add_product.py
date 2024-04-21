from flask import Blueprint, jsonify, request
from flask_mysqldb import MySQL

add_product_bp = Blueprint("add_product", __name__)

mysql = MySQL()


@add_product_bp.route("/api/add_product", methods=["POST"])
def add_product():
    try:
        product = request.get_json().get("product")
        category = product.get("category")
        description = product.get("description")
        image = product.get("image")
        price = product.get("price")
        title = product.get("title")
        
        cursor = mysql.connection.cursor()

        sql = "INSERT INTO products_table (category, description, image, price, title) VALUES (%s, %s, %s, %s, %s)"
        values = (
            category,
            description,
            image,
            price,
            title,
        )
        cursor.execute(sql, values)

        mysql.connection.commit()

        cursor.close()

        return jsonify({"productAdded": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
