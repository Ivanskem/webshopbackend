from flask import Blueprint, render_template, request
from app.extensions import db
from app.models.product import Product
from app.models.category import Category

bp = Blueprint('products', __name__)

@bp.route('/')
def product_list():
    page = request.args.get('page', 1, type=int)
    per_page = 12
    products = Product.query.paginate(page=page, per_page=per_page)
    categories = Category.query.all()
    return render_template('products/list.html', products=products, categories=categories)

@bp.route('/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('products/detail.html', product=product)