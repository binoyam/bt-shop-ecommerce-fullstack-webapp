from flask import Flask
from flask_cors import CORS
from flask_mysqldb import MySQL

# user routes
from routes.auth import auth_bp
from routes.feedback import feedback_bp
from routes.get_products import get_products_bp
from routes.place_orders import place_orders_bp
from routes.rate_product import rate_product_bp
from routes.helpers import get_product_ids

# admin routes
from routes.admin_routes.users import users_bp
from routes.admin_routes.orders import orders_bp
from routes.admin_routes.products import products_bp
from routes.admin_routes.remove_order import remove_order_bp
from routes.admin_routes.remove_user import remove_user_bp
from routes.admin_routes.remove_product import remove_product_bp
from routes.admin_routes.add_product import add_product_bp

app = Flask(__name__, static_folder="./dist", static_url_path="")
mysql = MySQL()
CORS(app)


app.config["SECRET_KEY"] = "YOUR_SECRET_KEY"
app.config["MYSQL_HOST"] = "sql11.freesqldatabase.com"
app.config["MYSQL_USER"] = "sql11700668"
app.config["MYSQL_PASSWORD"] = "CRLthh43hk"
app.config["MYSQL_DB"] = "sql11700668"
app.config["MYSQL_PORT"] = 3306

mysql.init_app(app)


@app.route("/")
@app.route("/contact")
@app.route("/about")
@app.route("/home")
@app.route("/products")
@app.route("/categories")
@app.route("/admin")
@app.route("/privacy-policy")
@app.route("/checkout")
@app.route("/payment")
@app.route("/categories/<string:subpath>")
def serve_static(subpath=None):
    if subpath in [
        "all",
        "mens-clothing",
        "womens-clothing",
        "electronics",
        "jewelery",
    ]:
        return app.send_static_file("index.html")
    return app.send_static_file("index.html")


@app.route("/products/<int:product_id>")
def product_id(product_id):
    try:
        id_list = get_product_ids()
        if product_id in id_list:
            return app.send_static_file("index.html")
        else:
            return "<h1 style='text-align:center'>Product not found</h1>"
    except Exception as e:
        return str(e)


# user routes
app.register_blueprint(auth_bp)
app.register_blueprint(feedback_bp)
app.register_blueprint(get_products_bp)
app.register_blueprint(place_orders_bp)
app.register_blueprint(rate_product_bp)
# admin routes
app.register_blueprint(users_bp)
app.register_blueprint(remove_user_bp)
app.register_blueprint(orders_bp)
app.register_blueprint(remove_order_bp)
app.register_blueprint(products_bp)
app.register_blueprint(remove_product_bp)
app.register_blueprint(add_product_bp)


if __name__ == "__main__":
    app.run(debug=True)
