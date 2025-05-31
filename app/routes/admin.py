from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from app.extensions import db
from app.models import User, Product, Order, Category
from app.utils.decorators import admin_required
from flask_admin import AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView

bp = Blueprint('admin_bp', __name__)

@bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    stats = {
        'users': User.query.count(),
        'products': Product.query.count(),
        'orders': Order.query.count(),
        'categories': Category.query.count()
    }
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
    return render_template('admin/dashboard.html', stats=stats, recent_orders=recent_orders)

@bp.route('/users')
@login_required
@admin_required
def manage_users():
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@bp.route('/products')
@login_required
@admin_required
def manage_products():
    products = Product.query.all()
    categories = Category.query.all()
    return render_template('admin/products.html', products=products, categories=categories)

@bp.route('/orders')
@login_required
@admin_required
def manage_orders():
    orders = Order.query.all()
    return render_template('admin/orders.html', orders=orders)

@bp.route('/categories')
@login_required
@admin_required
def manage_categories():
    categories = Category.query.all()
    return render_template('admin/categories.html', categories=categories)


class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

class UserAdminView(AdminModelView):
    column_list = ('id', 'username', 'email', 'is_admin', 'created_at')
    column_searchable_list = ('username', 'email')
    column_filters = ('is_admin',)
    form_columns = ('username', 'email', 'password_hash', 'is_admin')

class ProductAdminView(AdminModelView):
    column_list = ('id', 'name', 'price', 'stock', 'category')
    column_searchable_list = ('name',)
    column_filters = ('price', 'stock', 'category.name')
    form_columns = ('name', 'description', 'price', 'stock', 'image_url', 'category')

class OrderAdminView(AdminModelView):
    column_list = ('id', 'user', 'total', 'created_at', 'status')
    column_filters = ('status', 'user.username')
    form_columns = ('user', 'total', 'status')

class CategoryAdminView(AdminModelView):
    column_list = ('id', 'name', 'products_count')
    column_searchable_list = ('name',)
    
    def products_count(self, context, model, name):
        return len(model.products)


def init_admin(admin, app):
  
    class MyAdminIndexView(AdminIndexView):
        @expose('/')
        @login_required
        @admin_required
        def index(self):
            return self.render('admin/index.html')
    
    admin.index_view = MyAdminIndexView()
    
   
    admin.add_view(UserAdminView(User, db.session))
    admin.add_view(ProductAdminView(Product, db.session))
    admin.add_view(OrderAdminView(Order, db.session))
    admin.add_view(CategoryAdminView(Category, db.session))