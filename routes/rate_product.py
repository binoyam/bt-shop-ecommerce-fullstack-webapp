from flask import Blueprint, jsonify, request
from flask_mysqldb import MySQL

rate_product_bp = Blueprint("rate_product", __name__)

mysql = MySQL()


@rate_product_bp.route("/api/rate_product", methods=["POST"])
def rate_product():
    data = request.json
    product_id = data.get("product_id")
    rating = float(data.get("rating"))
    try:
        cursor = mysql.connection.cursor()
        select_query = (
            "SELECT `rating.count`, `rating.rate` FROM products_table WHERE id = %s"
        )

        cursor.execute(
            select_query,
            (product_id,),
        )
        rating_data = cursor.fetchone()
        prev_count = rating_data[0]
        prev_rating = rating_data[1]

        print(rating_data)
        if prev_count is None:
            prev_count = 0
            new_count = 1
        else:
            new_count = prev_count + 1
        if prev_rating is None:
            prev_rating = float(0)
            new_rating = rating / new_count
        else:
            new_rating = (prev_rating * prev_count + rating) / new_count

        new_rating_rounded = round(new_rating, 1)

        update_query = "UPDATE products_table SET `rating.count` = %s, `rating.rate` = %s WHERE id = %s"
        cursor.execute(
            update_query,
            (
                new_count,
                new_rating_rounded,
                product_id,
            ),
        )

        mysql.connection.commit()
        # check if updated correctly
        cursor.execute(select_query, (product_id,))
        updatedRating = cursor.fetchone()
        updated_count = updatedRating[0]
        updated_rating = updatedRating[1]
        print(updatedRating)
        cursor.close()

        if updated_rating == new_rating_rounded and updated_count == new_count:
            response_data = {"rateSubmited": True}
        else:
            response_data = {"rateSubmited": False}
        return jsonify(response_data)
    except Exception as e:
        return str(e), 500
