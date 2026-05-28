from email.headerregistry import Address

from flask import Flask, render_template, url_for, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import text
from flask_mail import Mail, Message

# ADMIN IMPORTS
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import os
# ---------------- APP INIT ----------------
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "glowcare_secret_2026")

from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "static/images"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# ---------------- DATABASE CONFIG ----------------
database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise RuntimeError("DATABASE_URL is not set")

if database_url.startswith("mysql://"):
    database_url = database_url.replace("mysql://", "mysql+pymysql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = database_url

app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "connect_args": {
        "ssl": {}
    }
}

database_url = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = os.getenv("SECRET_KEY", "glowcare_secret_2026")
# MAIL CONFIG
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")

db = SQLAlchemy(app)
mail = Mail(app)

# ---------------- ADMIN SECURITY ----------------
class AdminSecure(ModelView):
    def is_accessible(self):
        return "user_id" in session and session["user_id"] == 1

    def inaccessible_callback(self, name, **kwargs):
        return redirect("/login")
# ---------------- MODELS ----------------

class User(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Product(db.Model):
    __tablename__ = "products"

    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    description = db.Column(db.Text)
    price = db.Column(db.Float)
    image_url = db.Column(db.String(255))
    stock = db.Column(db.Integer, default=0)

class Order(db.Model):
    __tablename__ = "orders"
    order_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    total_amount = db.Column(db.Float)
    status = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class OrderItem(db.Model):
    __tablename__ = "order_items"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)

# ---------------- ADMIN SETUP ----------------
admin = Admin(app, name="GlowCare Admin")

class UserAdmin(AdminSecure):
    column_list = ["user_id", "name", "email", "created_at"]
    column_searchable_list = ["name", "email"]
    column_filters = ["created_at"]

    column_exclude_list = ["password"]   # hide password


class ProductAdmin(AdminSecure):

    column_list = [
        "product_id",
        "name",
        "price",
        "stock",
        "image_url"
    ]

    column_searchable_list = ["name"]

    column_filters = [
        "price",
        "stock"
    ]

    form_columns = [
        "name",
        "description",
        "price",
        "stock",
        "image_url"
    ]
class OrderAdmin(AdminSecure):
    column_list = ["order_id", "user_id", "total_amount", "status", "created_at"]

    column_filters = ["status", "created_at"]
    column_searchable_list = ["user_id"]

    form_choices = {
        "status": [
            ("Placed", "Placed"),
            ("Shipped", "Shipped"),
            ("Out for Delivery", "Out for Delivery"),
            ("Delivered", "Delivered"),
            ("Cancelled", "Cancelled")
        ]
    }
class OrderItemAdmin(AdminSecure):
    column_list = ["order_id", "product_id", "quantity", "price"]



admin.add_view(UserAdmin(User, db.session))
admin.add_view(ProductAdmin(Product, db.session))
admin.add_view(OrderAdmin(Order, db.session))
admin.add_view(OrderItemAdmin(OrderItem, db.session))

# ---------------- ROUTES ----------------
@app.route("/")
def home():
    return redirect(url_for("login"))

@app.route("/dashboard")
def dashboard():

    # SORT
    sort = request.args.get("sort")

    query = """
    SELECT
        p.*,
        IFNULL(AVG(r.rating), 0) AS avg_rating,
        COUNT(r.review_id) AS total_reviews

    FROM products p

    LEFT JOIN reviews r
    ON p.product_id = r.product_id

    GROUP BY p.product_id
    """

    if sort == "low":
        query += " ORDER BY price ASC"

    elif sort == "high":
        query += " ORDER BY price DESC"

    elif sort == "new":
        query += " ORDER BY product_id DESC"

    # PAGINATION
    page = request.args.get("page", 1, type=int)

    per_page = 8

    offset = (page - 1) * per_page

    query += f" LIMIT {per_page} OFFSET {offset}"

    # PRODUCTS
    products = db.session.execute(text(query)).fetchall()

    # TOTAL PRODUCTS
    total_products = db.session.execute(text("""
        SELECT COUNT(*) FROM products
    """)).fetchone()[0]

    total_pages = (total_products + per_page - 1) // per_page

    # WISHLIST
    wishlist_ids = []

    if "user_id" in session:

        data = db.session.execute(text("""
            SELECT product_id
            FROM wishlist
            WHERE user_id=:uid
        """), {
            "uid": session["user_id"]
        }).fetchall()

        wishlist_ids = [i[0] for i in data]

    # CONCERNS
    concerns = db.session.execute(text("""
        SELECT * FROM concerns
    """)).fetchall()

    # INGREDIENTS
    ingredients = db.session.execute(text("""
        SELECT * FROM ingredients
    """)).fetchall()

    return render_template(
        "dashboard.html",
        products=products,
        wishlist_ids=wishlist_ids,
        concerns=concerns,
        ingredients=ingredients,
        page=page,
        total_pages=total_pages
    )
# ---------------- AUTH ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = User(
            name=request.form["name"],
            email=request.form["email"],
            password=generate_password_hash(request.form["password"])
        )
        db.session.add(user)
        db.session.commit()
        return redirect("/login")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(email=request.form["email"]).first()

        if user and check_password_hash(user.password, request.form["password"]):
            session["user_id"] = user.user_id
            return redirect("/dashboard")

        return "Invalid credentials"

    return render_template("login.html")


# ---------------- FILTER ----------------
@app.route("/filter/ingredient/<path:name>")
def filter_ingredient(name):

    products = db.session.execute(text("""
    
        SELECT
            p.product_id,
            p.name,
            p.description,
            p.price,
            p.stock,
            p.image_url,

            IFNULL(AVG(r.rating), 0) AS avg_rating,
            COUNT(r.review_id) AS total_reviews

        FROM products p

        JOIN product_ingredients pi
        ON p.product_id = pi.product_id

        JOIN ingredients i
        ON pi.ingredient_id = i.ingredient_id

        LEFT JOIN reviews r
        ON p.product_id = r.product_id

        WHERE i.name = :name

        GROUP BY
            p.product_id,
            p.name,
            p.description,
            p.price,
            p.stock,
            p.image_url

    """), {
        "name": name
    }).fetchall()

    concerns = db.session.execute(text("""
        SELECT * FROM concerns
    """)).fetchall()

    ingredients = db.session.execute(text("""
        SELECT * FROM ingredients
    """)).fetchall()

    wishlist_ids = []

    if "user_id" in session:

        data = db.session.execute(text("""
        
            SELECT product_id
            FROM wishlist
            WHERE user_id = :uid
        
        """), {
            "uid": session["user_id"]
        }).fetchall()

        wishlist_ids = [i[0] for i in data]

    return render_template(
        "dashboard.html",
        products=products,
        concerns=concerns,
        ingredients=ingredients,
        wishlist_ids=wishlist_ids,
        page=1,
        total_pages=1
    )
    

@app.route("/filter/concern/<path:name>")
def filter_concern(name):

    products = db.session.execute(text("""
    SELECT
        p.*,
        IFNULL(AVG(r.rating), 0) AS avg_rating

    FROM products p

    JOIN product_concerns pc
    ON p.product_id = pc.product_id

    JOIN concerns c
    ON pc.concern_id = c.concern_id

    LEFT JOIN reviews r
    ON p.product_id = r.product_id

    WHERE c.name = :name

    GROUP BY p.product_id
    """), {
        "name": name
    }).fetchall()

    concerns = db.session.execute(text("""
        SELECT * FROM concerns
    """)).fetchall()

    ingredients = db.session.execute(text("""
        SELECT * FROM ingredients
    """)).fetchall()

    wishlist_ids = []

    if "user_id" in session:

        data = db.session.execute(text("""
            SELECT product_id
            FROM wishlist
            WHERE user_id = :uid
        """), {
            "uid": session["user_id"]
        }).fetchall()

        wishlist_ids = [i[0] for i in data]

    return render_template(
        "dashboard.html",
        products=products,
        concerns=concerns,
        ingredients=ingredients,
        wishlist_ids=wishlist_ids,
        page=1,
        total_pages=1
    )

    

# ---------------- SEARCH ----------------
@app.route("/search")
def search():

    q = request.args.get("q")

    products = db.session.execute(text("""
    SELECT
        p.*,
        IFNULL(AVG(r.rating), 0) AS avg_rating

    FROM products p

    LEFT JOIN reviews r
    ON p.product_id = r.product_id

    WHERE p.name LIKE :q
    OR p.description LIKE :q

    GROUP BY p.product_id
    """), {
        "q": f"%{q}%"
    }).fetchall()

    concerns = db.session.execute(text("""
        SELECT * FROM concerns
    """)).fetchall()

    ingredients = db.session.execute(text("""
        SELECT * FROM ingredients
    """)).fetchall()

    wishlist_ids = []

    if "user_id" in session:

        data = db.session.execute(text("""
            SELECT product_id
            FROM wishlist
            WHERE user_id=:uid
        """), {
            "uid": session["user_id"]
        }).fetchall()

        wishlist_ids = [i[0] for i in data]

    return render_template(
        "dashboard.html",
        products=products,
        concerns=concerns,
        ingredients=ingredients,
        wishlist_ids=wishlist_ids,
        page=1,
        total_pages=1
    )

    
# ---------------- CART PAGE ----------------
@app.route("/cart")
def cart():
    return render_template("cart.html")


# ---------------- CART APIs ----------------
@app.route("/api/cart/add", methods=["POST"])
def add_to_cart():
    if "user_id" not in session:
        return {"error": "Login required"}, 401

    user_id = session["user_id"]
    product_id = request.json["product_id"]

    existing = db.session.execute(text("""
        SELECT * FROM cart WHERE user_id=:u AND product_id=:p
    """), {"u": user_id, "p": product_id}).fetchone()

    if existing:
        db.session.execute(text("""
            UPDATE cart SET quantity = quantity + 1
            WHERE user_id=:u AND product_id=:p
        """), {"u": user_id, "p": product_id})
    else:
        db.session.execute(text("""
            INSERT INTO cart (user_id, product_id, quantity)
            VALUES (:u, :p, 1)
        """), {"u": user_id, "p": product_id})

    db.session.commit()
    return {"message": "Added"}


@app.route("/api/cart")
def get_cart():
    if "user_id" not in session:
        return []

    user_id = session["user_id"]

    data = db.session.execute(text("""
        SELECT c.cart_id, p.name, p.price, p.image_url, c.quantity
        FROM cart c
        JOIN products p ON c.product_id = p.product_id
        WHERE c.user_id = :uid
    """), {"uid": user_id}).fetchall()

    return [{
        "cart_id": i[0],
        "name": i[1],
        "price": float(i[2]),
        "image": i[3],
        "quantity": i[4]
    } for i in data]


@app.route("/api/cart/update", methods=["POST"])
def update_cart():
    data = request.json

    if data["quantity"] <= 0:
        db.session.execute(text("DELETE FROM cart WHERE cart_id=:id"),
                           {"id": data["cart_id"]})
    else:
        db.session.execute(text("""
            UPDATE cart SET quantity=:q WHERE cart_id=:id
        """), {"q": data["quantity"], "id": data["cart_id"]})

    db.session.commit()
    return {"message": "updated"}


# ---------------- CHECKOUT ----------------
@app.route("/checkout")
def checkout():

    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    # 🛒 CART ITEMS
    cart_items = db.session.execute(text("""
        SELECT p.name, p.price, c.quantity
        FROM cart c
        JOIN products p ON c.product_id = p.product_id
        WHERE c.user_id = :uid
    """), {"uid": user_id}).fetchall()

    # 💰 TOTAL
    total = sum(i[1] * i[2] for i in cart_items)

    discount = 0
    coupon_code = request.args.get("coupon")

    if coupon_code:
        coupon = db.session.execute(text("""
            SELECT discount_percent
            FROM coupons
            WHERE code = :code
            AND active = TRUE
        """), {
            "code": coupon_code
        }).fetchone()

        if coupon:
            discount = (total * coupon[0]) / 100
            total = total - discount

    # 📍 ADDRESSES
    addresses = db.session.execute(text("""
        SELECT * FROM addresses WHERE user_id = :uid
    """), {"uid": user_id}).fetchall()

    return render_template(
        "checkout.html",
        cart_items=cart_items,
        total=total,
        discount=discount,
        coupon_code=coupon_code,
        addresses=addresses
    )


@app.route("/api/checkout", methods=["POST"])
def checkout_api():

    if "user_id" not in session:
        return {"error": "Login required"}, 401

    user_id = session["user_id"]

    cart_items = db.session.execute(text("""
        SELECT c.product_id, c.quantity, p.price
        FROM cart c
        JOIN products p ON c.product_id = p.product_id
        WHERE c.user_id = :uid
    """), {"uid": user_id}).fetchall()

    if not cart_items:
        return {"error": "Cart empty"}

    total = sum(i[1] * float(i[2]) for i in cart_items)

    result = db.session.execute(text("""
        INSERT INTO orders (user_id, total_amount, status)
        VALUES (:uid, :total, 'Placed')
    """), {"uid": user_id, "total": total})

    order_id = result.lastrowid

    for item in cart_items:
        db.session.execute(text("""
            INSERT INTO order_items (order_id, product_id, quantity, price)
            VALUES (:oid, :pid, :qty, :price)
        """), {
            "oid": order_id,
            "pid": item[0],
            "qty": item[1],
            "price": item[2]
        })

    db.session.execute(text("DELETE FROM cart WHERE user_id=:uid"),
                       {"uid": user_id})

    db.session.commit()

    return {
    "message": "Order placed successfully",
    "order_id": order_id
}
# ---------------- PRODUCT PAGE ----------------
@app.route("/product/<int:id>")
def product_detail(id):

    # PRODUCT
    product = db.session.execute(text("""
        SELECT * FROM products
        WHERE product_id = :id
    """), {"id": id}).fetchone()

    # REVIEWS
    reviews = db.session.execute(text("""
        SELECT r.rating, r.comment, u.name
        FROM reviews r
        JOIN users u
        ON r.user_id = u.user_id
        WHERE r.product_id = :id
    """), {"id": id}).fetchall()
    # ⭐ RATING SUMMARY
    rating_data = db.session.execute(text("""
    SELECT
        IFNULL(AVG(rating), 0),
        COUNT(*)

    FROM reviews

    WHERE product_id = :id
        """), {
    "id": id
    }).fetchone()

    # INGREDIENTS
    ingredients = db.session.execute(text("""
        SELECT i.name
        FROM product_ingredients pi
        JOIN ingredients i
        ON pi.ingredient_id = i.ingredient_id
        WHERE pi.product_id = :id
    """), {"id": id}).fetchall()

    # CONCERNS
    concerns = db.session.execute(text("""
        SELECT c.name
        FROM product_concerns pc
        JOIN concerns c
        ON pc.concern_id = c.concern_id
        WHERE pc.product_id = :id
    """), {"id": id}).fetchall()

    # RELATED PRODUCTS
    related_products = db.session.execute(text("""
        SELECT DISTINCT p.*
        FROM products p
        JOIN product_concerns pc
        ON p.product_id = pc.product_id

        WHERE pc.concern_id IN (

            SELECT concern_id
            FROM product_concerns
            WHERE product_id = :id

        )

        AND p.product_id != :id

        LIMIT 4
    """), {"id": id}).fetchall()

    return render_template(
    "product.html",
    product=product,
    reviews=reviews,
    ingredients=ingredients,
    concerns=concerns,
    related_products=related_products,
    rating_data=rating_data
)


# ---------------- REVIEWS ----------------
@app.route("/add_review/<int:product_id>", methods=["POST"])
def add_review(product_id):

    if "user_id" not in session:
        return redirect("/login")

    db.session.execute(text("""
        INSERT INTO reviews (user_id, product_id, rating, comment)
        VALUES (:u, :p, :r, :c)
    """), {
        "u": session["user_id"],
        "p": product_id,
        "r": request.form["rating"],
        "c": request.form["review"]
    })

    db.session.commit()

    return redirect(url_for("product_detail", id=product_id))
# ---------------- ABOUT ----------------
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/orders")
def orders():

    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    orders = db.session.execute(text("""
        SELECT * FROM orders
        WHERE user_id = :uid
        ORDER BY created_at DESC
    """), {"uid": user_id}).fetchall()

    return render_template("orders.html", orders=orders)


@app.route("/api/order-items/<int:order_id>")
def order_items(order_id):

    items = db.session.execute(text("""
        SELECT p.name, p.image_url, oi.quantity, oi.price
        FROM order_items oi
        JOIN products p ON oi.product_id = p.product_id
        WHERE oi.order_id = :oid
    """), {"oid": order_id}).fetchall()

    return [
        {
            "name": i[0],
            "image": i[1],
            "quantity": i[2],
            "price": float(i[3])
        } for i in items
    ]


@app.route("/orders-data")
def orders_data():

    if "user_id" not in session:
        return []

    user_id = session["user_id"]

    orders = db.session.execute(text("""
        SELECT order_id, total_amount, status
        FROM orders
        WHERE user_id = :uid
        ORDER BY order_id DESC
    """), {"uid": user_id}).fetchall()

    return [
        {
            "order_id": o[0],
            "total": float(o[1]),
            "status": o[2]
        } for o in orders
    ]

@app.route("/success/<int:order_id>")
def success(order_id):

    # 📦 ORDER INFO
    order = db.session.execute(text("""
        SELECT total_amount, status, address_id
        FROM orders
        WHERE order_id = :oid
    """), {"oid": order_id}).fetchone()

    # 🧾 ORDER ITEMS
    items = db.session.execute(text("""
        SELECT p.name, p.image_url, oi.quantity, oi.price
        FROM order_items oi
        JOIN products p ON oi.product_id = p.product_id
        WHERE oi.order_id = :oid
    """), {"oid": order_id}).fetchall()

    # 📍 ADDRESS (THIS WAS MISSING)
    address = db.session.execute(text("""
        SELECT full_address, city, pincode
        FROM addresses
        WHERE address_id = :aid
    """), {"aid": order[2]}).fetchone()

    # 📅 DELIVERY DATE
    delivery_date = (datetime.now() + timedelta(days=4)).strftime("%d %b %Y")

    return render_template(
        "success.html",
        order_id=order_id,
        order=order,
        items=items,
        delivery_date=delivery_date,
        address=address   
    )



@app.route("/profile")
def profile():

    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    # 👤 USER INFO
    user = db.session.execute(text("""
        SELECT name, email, created_at
        FROM users
        WHERE user_id = :uid
    """), {"uid": user_id}).fetchone()

    # 📦 TOTAL ORDERS
    total_orders = db.session.execute(text("""
        SELECT COUNT(*) FROM orders
        WHERE user_id = :uid
    """), {"uid": user_id}).fetchone()[0]

    # 💰 TOTAL SPENT
    total_spent = db.session.execute(text("""
        SELECT IFNULL(SUM(total_amount), 0)
        FROM orders
        WHERE user_id = :uid
    """), {"uid": user_id}).fetchone()[0]

    # 📍 ADDRESSES
    addresses = db.session.execute(text("""
        SELECT * FROM addresses
        WHERE user_id = :uid
    """), {"uid": user_id}).fetchall()

    # 💳 PAYMENTS
    payments = db.session.execute(text("""
        SELECT * FROM payments
        WHERE user_id = :uid
    """), {"uid": user_id}).fetchall()

    # 🧾 ORDERS LIST (history)
    orders = db.session.execute(text("""
        SELECT order_id, total_amount, status
        FROM orders
        WHERE user_id = :uid
        ORDER BY order_id DESC
    """), {"uid": user_id}).fetchall()

    # ❤️ WISHLIST
    wishlist = db.session.execute(text("""
        SELECT p.product_id, p.name, p.price, p.image_url
        FROM wishlist w
        JOIN products p ON w.product_id = p.product_id
        WHERE w.user_id = :uid
    """), {"uid": user_id}).fetchall()

    return render_template(
        "profile.html",
        user=user,
        total_orders=total_orders,
        total_spent=total_spent,
        addresses=addresses,
        payments=payments,
        orders=orders,
        wishlist=wishlist
    )

@app.route("/add-address", methods=["POST"])
def add_address():
    db.session.execute(text("""
        INSERT INTO addresses (user_id, full_address, city, pincode)
        VALUES (:u, :a, :c, :p)
    """), {
        "u": session["user_id"],
        "a": request.form["address"],
        "c": request.form["city"],
        "p": request.form["pincode"]
    })

    db.session.commit()
    return redirect("/profile")


@app.route("/add-payment", methods=["POST"])
def add_payment():
    db.session.execute(text("""
        INSERT INTO payments (user_id, method, details)
        VALUES (:u, :m, :d)
    """), {
        "u": session["user_id"],
        "m": request.form["method"],
        "d": request.form["details"]
    })

    db.session.commit()
    return redirect("/profile")




@app.route("/api/wishlist/add", methods=["POST"])
def add_wishlist():

    if "user_id" not in session:
        return {"error": "Login required"}, 401

    db.session.execute(text("""
        INSERT INTO wishlist (user_id, product_id)
        VALUES (:u, :p)
    """), {
        "u": session["user_id"],
        "p": request.json["product_id"]
    })

    db.session.commit()

    return {"message": "added"}
@app.route("/wishlist")
def wishlist():

    if "user_id" not in session:
        return redirect("/login")

    items = db.session.execute(text("""
        SELECT p.* FROM wishlist w
        JOIN products p ON w.product_id = p.product_id
        WHERE w.user_id = :uid
    """), {"uid": session["user_id"]}).fetchall()

    return render_template("wishlist.html", items=items)


@app.route("/api/wishlist/toggle", methods=["POST"])
def toggle_wishlist():

    if "user_id" not in session:
        return {"error": "Login required"}, 401

    user_id = session["user_id"]
    product_id = request.json["product_id"]

    # check if already exists
    exists = db.session.execute(text("""
        SELECT 1 FROM wishlist
        WHERE user_id=:uid AND product_id=:pid
    """), {
        "uid": user_id,
        "pid": product_id
    }).fetchone()

    if exists:
        # ❌ REMOVE
        db.session.execute(text("""
            DELETE FROM wishlist
            WHERE user_id=:uid AND product_id=:pid
        """), {
            "uid": user_id,
            "pid": product_id
        })

        db.session.commit()
        return {"status": "removed"}

    else:
        # ✅ ADD
        db.session.execute(text("""
            INSERT INTO wishlist (user_id, product_id)
            VALUES (:uid, :pid)
        """), {
            "uid": user_id,
            "pid": product_id
        })

        db.session.commit()
        return {"status": "added"}



@app.route("/place-order", methods=["POST"])
def place_order():

    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    address_id = request.form.get("address_id")

    # 👉 ADD NEW ADDRESS
    if request.form.get("new_address"):

        result = db.session.execute(text("""
            INSERT INTO addresses
            (
                user_id,
                full_address,
                city,
                pincode
            )

            VALUES
            (
                :u,
                :a,
                :c,
                :p
            )
        """), {
            "u": user_id,
            "a": request.form["new_address"],
            "c": request.form["city"],
            "p": request.form["pincode"]
        })

        db.session.commit()

        address_id = result.lastrowid

    # 🛒 CART ITEMS
    cart_items = db.session.execute(text("""
        SELECT
            c.product_id,
            c.quantity,
            p.price,
            p.stock

        FROM cart c

        JOIN products p
        ON c.product_id = p.product_id

        WHERE c.user_id = :uid
    """), {
        "uid": user_id
    }).fetchall()

    # ❌ EMPTY CART
    if not cart_items:
        return "Cart is empty"

    # ❌ STOCK CHECK
    for item in cart_items:

        quantity = item[1]
        stock = item[3]

        if quantity > stock:
            return "Some products are out of stock"

    # 💰 TOTAL
    total = sum(
        item[1] * float(item[2])
        for item in cart_items
    )

    # 📦 CREATE ORDER
    result = db.session.execute(text("""
        INSERT INTO orders
        (
            user_id,
            total_amount,
            status,
            address_id
        )

        VALUES
        (
            :uid,
            :total,
            'Placed',
            :aid
        )
    """), {
        "uid": user_id,
        "total": total,
        "aid": address_id
    })

    order_id = result.lastrowid

    # 🧾 ORDER ITEMS + STOCK UPDATE
    for item in cart_items:

        product_id = item[0]
        quantity = item[1]
        price = item[2]

        # INSERT ORDER ITEM
        db.session.execute(text("""
            INSERT INTO order_items
            (
                order_id,
                product_id,
                quantity,
                price
            )

            VALUES
            (
                :oid,
                :pid,
                :qty,
                :price
            )
        """), {
            "oid": order_id,
            "pid": product_id,
            "qty": quantity,
            "price": price
        })

        # UPDATE STOCK
        db.session.execute(text("""
            UPDATE products

            SET stock = stock - :qty

            WHERE product_id = :pid
        """), {
            "qty": quantity,
            "pid": product_id
        })

    # 🧹 CLEAR CART
    db.session.execute(text("""
        DELETE FROM cart
        WHERE user_id = :uid
    """), {
        "uid": user_id
    })

    # ✅ SAVE CHANGES
    db.session.commit()

    # 👤 USER INFO
    user = db.session.execute(text("""
        SELECT email, name

        FROM users

        WHERE user_id = :uid
    """), {
        "uid": user_id
    }).fetchone()

    # 📧 EMAIL
    try:

        msg = Message(
            subject="Order Confirmed - GlowCare",
            sender=app.config["MAIL_USERNAME"],
            recipients=[user.email]
        )

        msg.body = f"""
Hello {user.name},

Your order has been placed successfully.

Order ID: {order_id}

Total Amount: ₹{total}

Thank you for shopping with GlowCare.
"""

        mail.send(msg)

    except Exception as e:
        print("Email Error:", e)

    return redirect(f"/success/{order_id}")

    
   

@app.route("/admin/add-product", methods=["GET", "POST"])
def add_product():

    # admin protection
    if "user_id" not in session or session["user_id"] != 1:
        return redirect("/login")

    # ingredients
    ingredients = db.session.execute(text("""
        SELECT * FROM ingredients
    """)).fetchall()

    # concerns
    concerns = db.session.execute(text("""
        SELECT * FROM concerns
    """)).fetchall()

    if request.method == "POST":

        name = request.form["name"]
        description = request.form["description"]
        price = request.form["price"]
        stock = request.form["stock"]

        # image
        image = request.files["image"]

        filename = secure_filename(image.filename)

        image.save(
            os.path.join(
                app.config["UPLOAD_FOLDER"],
                filename
            )
        )

        # INSERT PRODUCT
        result = db.session.execute(text("""
            INSERT INTO products
            (
                name,
                description,
                price,
                image_url,
                stock
            )

            VALUES
            (
                :n,
                :d,
                :p,
                :i,
                :s
            )
        """), {
            "n": name,
            "d": description,
            "p": price,
            "i": filename,
            "s": stock
        })

        db.session.commit()

        product_id = result.lastrowid

        # INGREDIENTS
        ingredient_ids = request.form.getlist("ingredients")

        for ingredient_id in ingredient_ids:

            db.session.execute(text("""
                INSERT INTO product_ingredients
                (
                    product_id,
                    ingredient_id
                )

                VALUES
                (
                    :p,
                    :i
                )
            """), {
                "p": product_id,
                "i": ingredient_id
            })

        # CONCERNS
        concern_ids = request.form.getlist("concerns")

        for concern_id in concern_ids:

            db.session.execute(text("""
                INSERT INTO product_concerns
                (
                    product_id,
                    concern_id
                )

                VALUES
                (
                    :p,
                    :c
                )
            """), {
                "p": product_id,
                "c": concern_id
            })

        db.session.commit()

        return redirect("/dashboard")

    return render_template(
        "add_products.html",
        ingredients=ingredients,
        concerns=concerns
    )




















































# ---------------- INIT ----------------


if __name__ == "__main__":
    app.run(debug=True)