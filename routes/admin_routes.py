import os
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    current_app,
)
from werkzeug.utils import secure_filename

from models.models import db, Product, Order, Category, OrderItem
from utils.helpers import admin_required

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def allowed_file(filename: str) -> bool:
    if "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[1].lower()
    return ext in current_app.config["ALLOWED_IMAGE_EXTENSIONS"]


@admin_bp.route("/")
@admin_required
def admin_dashboard():
    total_products = Product.query.count()
    total_orders = Order.query.count()
    pending_orders = Order.query.filter_by(status="Pending").count()
    delivered_orders = Order.query.filter_by(status="Delivered").count()
    return render_template(
        "admin/admin_dashboard.html",
        total_products=total_products,
        total_orders=total_orders,
        pending_orders=pending_orders,
        delivered_orders=delivered_orders,
    )


# -------- PRODUCTS (CRUD) -------- #

@admin_bp.route("/products")
@admin_required
def manage_products():
    products = Product.query.order_by(Product.id.desc()).all()
    categories = Category.query.order_by(Category.name).all()
    return render_template(
        "admin/manage_products.html",
        products=products,
        categories=categories,
    )


@admin_bp.route("/products/create", methods=["POST"])
@admin_required
def create_product():
    name = request.form.get("name")
    price = float(request.form.get("price"))
    stock = int(request.form.get("stock"))
    category_name = request.form.get("category") or "General"
    description = request.form.get("description")

    # category
    category = Category.query.filter_by(name=category_name).first()
    if not category:
        category = Category(name=category_name)
        db.session.add(category)
        db.session.flush()

    image_file = request.files.get("image")
    filename = None
    if image_file and image_file.filename:
        if allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            save_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
            image_file.save(save_path)
        else:
            flash("Invalid image type.", "danger")

    product = Product(
        name=name,
        description=description,
        price=price,
        stock=stock,
        category_id=category.id,
        image=filename,
    )
    db.session.add(product)
    db.session.commit()

    flash("Product added successfully!", "success")
    return redirect(url_for("admin.manage_products"))


@admin_bp.route("/products/<int:product_id>/update", methods=["POST"])
@admin_required
def update_product(product_id):
    product = Product.query.get_or_404(product_id)

    product.name = request.form.get("name")
    product.price = float(request.form.get("price"))
    product.stock = int(request.form.get("stock"))
    product.description = request.form.get("description")
    category_name = request.form.get("category") or "General"

    category = Category.query.filter_by(name=category_name).first()
    if not category:
        category = Category(name=category_name)
        db.session.add(category)
        db.session.flush()
    product.category_id = category.id

    image_file = request.files.get("image")
    if image_file and image_file.filename:
        if allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            save_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
            image_file.save(save_path)
            product.image = filename
        else:
            flash("Invalid image type. Old image kept.", "warning")

    db.session.commit()
    flash("Product updated.", "success")
    return redirect(url_for("admin.manage_products"))


@admin_bp.route("/products/<int:product_id>/delete", methods=["POST"])
@admin_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)

    # If you want to also delete image file, you can do it here (optional)
    db.session.delete(product)
    db.session.commit()
    flash("Product deleted.", "info")
    return redirect(url_for("admin.manage_products"))


# -------- ORDERS MANAGEMENT -------- #

@admin_bp.route("/orders", methods=["GET", "POST"])
@admin_required
def manage_orders():
    if request.method == "POST":
        order_id = int(request.form.get("order_id"))
        new_status = request.form.get("status")
        order = Order.query.get_or_404(order_id)
        order.status = new_status
        db.session.commit()
        flash("Order status updated.", "success")
        return redirect(url_for("admin.manage_orders"))

    status_filter = request.args.get("status", "")
    query = Order.query

    if status_filter:
        query = query.filter_by(status=status_filter)

    orders = query.order_by(Order.created_at.desc()).all()
    all_statuses = ["Pending", "Shipped", "Delivered"]

    return render_template(
        "admin/manage_orders.html",
        orders=orders,
        all_statuses=all_statuses,
        selected_status=status_filter,
    )


@admin_bp.route("/orders/<int:order_id>")
@admin_required
def order_detail(order_id):
    order = Order.query.get_or_404(order_id)
    items = (
        OrderItem.query.filter_by(order_id=order.id)
        .join(Product, Product.id == OrderItem.product_id)
        .all()
    )
    return render_template("admin/order_detail.html", order=order, items=items)
