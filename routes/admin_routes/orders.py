from flask import Blueprint
from flask_mysqldb import MySQL
from routes.helpers import convert_to_objects

orders_bp = Blueprint("orders", __name__)

mysql = MySQL()
# get all users for admin page

@orders_bp.route("/api/orders")
def get_orders():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM orders_table")
    orders = convert_to_objects(cursor)
    cursor.close()
    # print(orders)
    return orders

