from flask import Blueprint, redirect, url_for, session, flash, render_template, request
from models.models import db, CartItem, Product, Order, OrderItem
from utils.helpers import login_required

cart_bp = Blueprint("cart", __name__)


@cart_bp.route("/add_to_cart/<int:product_id>")
@login_required
def add_to_cart(product_id):
    user_id = session["user_id"]
    product = Product.query.get_or_404(product_id)

    if product.stock <= 0:
        flash("Product is out of stock!", "danger")
        return redirect(url_for("products.product_list"))

    item = CartItem.query.filter_by(user_id=user_id, product_id=product_id).first()

    if item:
        if item.quantity < product.stock:
            item.quantity += 1
        else:
            flash("You already added maximum available stock.", "warning")
            return redirect(url_for("products.product_list"))
    else:
        item = CartItem(user_id=user_id, product_id=product_id, quantity=1)
        db.session.add(item)

    db.session.commit()
    flash("Added to cart!", "success")
    return redirect(url_for("products.product_list"))


@cart_bp.route("/cart")
@login_required
def view_cart():
    user_id = session["user_id"]
    cart_items = CartItem.query.filter_by(user_id=user_id).all()
    total = sum(ci.quantity * ci.product.price for ci in cart_items)

    return render_template("cart.html", cart_items=cart_items, total=total)


@cart_bp.route("/update_cart", methods=["POST"])
@login_required
def update_cart():
    user_id = session["user_id"]

    for key, value in request.form.items():
        if key.startswith("qty_"):
            item_id = int(key.split("_")[1])
            qty = max(int(value), 0)

            item = CartItem.query.filter_by(id=item_id, user_id=user_id).first()
            if item:
                if qty == 0:
                    db.session.delete(item)
                else:
                    # don't exceed available stock
                    if qty > item.product.stock:
                        qty = item.product.stock
                        flash(
                            f"Reduced quantity for {item.product.name} due to limited stock.",
                            "warning",
                        )
                    item.quantity = qty

    db.session.commit()
    flash("Cart updated!", "success")
    return redirect(url_for("cart.view_cart"))


@cart_bp.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    user_id = session["user_id"]
    cart_items = CartItem.query.filter_by(user_id=user_id).all()

    if not cart_items:
        flash("Your cart is empty.", "warning")
        return redirect(url_for("products.product_list"))

    total = sum(ci.quantity * ci.product.price for ci in cart_items)

    if request.method == "POST":
        # Check stock before creating order
        for ci in cart_items:
            if ci.product.stock < ci.quantity:
                flash(f"Not enough stock for {ci.product.name}", "danger")
                return redirect(url_for("cart.view_cart"))

        order = Order(user_id=user_id, total_amount=total, status="Pending")
        db.session.add(order)
        db.session.flush()  # assign order.id

        for ci in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=ci.product_id,
                quantity=ci.quantity,
                price=ci.product.price,
            )
            ci.product.stock -= ci.quantity
            db.session.add(order_item)
            db.session.delete(ci)

        db.session.commit()
        flash("Order placed successfully!", "success")
        return redirect(url_for("cart.orders"))

    return render_template("checkout.html", cart_items=cart_items, total=total)


@cart_bp.route("/orders")
@login_required
def orders():
    user_id = session["user_id"]
    user_orders = (
        Order.query.filter_by(user_id=user_id)
        .order_by(Order.created_at.desc())
        .all()
    )
    return render_template("orders.html", orders=user_orders)
