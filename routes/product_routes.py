from flask import Blueprint, render_template, request
from models.models import Product, Category

product_bp = Blueprint("products", __name__)


@product_bp.route("/products")
def product_list():
    q = request.args.get("q", "").strip()
    category_id = request.args.get("category", type=int)

    query = Product.query

    if q:
        like_q = f"%{q}%"
        query = query.filter(Product.name.ilike(like_q) | Product.description.ilike(like_q))

    if category_id:
        query = query.filter(Product.category_id == category_id)

    items = query.order_by(Product.id.desc()).all()
    categories = Category.query.order_by(Category.name).all()

    return render_template(
        "products.html",
        items=items,
        categories=categories,
        selected_category=category_id,
        search_query=q,
    )
