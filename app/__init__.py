from flask import Flask
from app.config import Config
from app.extensions import db, login_manager, migrate, admin
from app.routes.auth import bp as auth_bp
from app.routes.main import bp as main_bp
from app.routes.products import bp as products_bp
from app.routes.cart import bp as cart_bp
from app.routes.admin import bp as admin_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    admin.init_app(app)
    
    
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(products_bp, url_prefix='/products')
    app.register_blueprint(cart_bp, url_prefix='/cart')
    app.register_blueprint(admin_bp, url_prefix='/admin', name='admin_bp')
    
    return app