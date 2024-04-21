from flask import Blueprint, jsonify, request
from flask_mysqldb import MySQL
from routes.helpers import insert_orders, merge_duplicates, fetch_orders

place_orders_bp = Blueprint("place_orders", __name__)

mysql = MySQL()


@place_orders_bp.route("/api/place_orders", methods=["POST"])
def place_order():
    data = request.json
    # print("data", data)
    customer_data = data.get("customerData")
    products_list = data.get("cartItemData")
    # print("products_list", products_list)
    customer_id = customer_data.get("customerId")
    customer_name = customer_data.get("customerName")
    customer_email = customer_data.get("customerEmail")

    insert_orders(customer_id, customer_name, customer_email, products_list)
    order_items = fetch_orders(customer_id)
    merged_items = merge_duplicates(order_items)
    # print("merged_items", merged_items)

    if merged_items:
        response_data = {
            "isOrderPlaced": True,
            "orderedItems": merged_items,
        }
    else:
        response_data = {
            "isOrderPlaced": False,
        }
    return jsonify(response_data)
