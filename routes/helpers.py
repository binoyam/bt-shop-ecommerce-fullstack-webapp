from flask import jsonify
from flask_mysqldb import MySQL


mysql = MySQL()


def convert_to_objects(cursor):
    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()
    objects = [dict(zip(columns, row)) for row in rows]
    return objects


def merge_duplicates(order_items):
    merged_items = {}
    for item in order_items:
        product_id = item["productId"]
        quantity = item["quantity"]
        if product_id in merged_items:
            merged_items[product_id]["quantity"] += quantity
        else:
            merged_items[product_id] = item

    merged_order_items = list(merged_items.values())
    return merged_order_items


def insert_orders(customer_id, customer_name, customer_email, products_list):
    cursor = mysql.connection.cursor()

    for product in products_list:
        product_id = product.get("productId")
        quantity = product.get("quantity")
        product_name = product.get("title")
        product_price = product.get("price")

        cursor.execute(
            "INSERT INTO orders_table (user_id, user_name, user_email, product_id, product_name, price, quantity) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (
                customer_id,
                customer_name,
                customer_email,
                product_id,
                product_name,
                product_price,
                quantity,
            ),
        )

        mysql.connection.commit()


def fetch_orders(customer_id):
    cursor = mysql.connection.cursor()

    cursor.execute(
        "SELECT * FROM orders_table WHERE user_id = %s",
        (customer_id,),
    )

    order_items = []
    orders_list = cursor.fetchall()
    for order in orders_list:
        order_id = order[0]
        user_id = order[1]
        user_name = order[2]
        user_email = order[3]
        product_id = order[4]
        product_name = order[5]
        price = order[6]
        quantity = order[7]
        order_items.append(
            {
                "orderId": order_id,
                "userId": user_id,
                "userName": user_name,
                "userEmail": user_email,
                "productId": product_id,
                "productName": product_name,
                "price": price,
                "quantity": quantity,
            }
        )

    return order_items


def get_product_ids():
    try:
        with mysql.connection.cursor() as cursor:
            cursor.execute("SELECT id FROM products_table")
            ids = cursor.fetchall()
            id_list = [id[0] for id in ids]
            return id_list

    except Exception as e:
        print(f"Error retrieving product IDs: {str(e)}")
        return []
