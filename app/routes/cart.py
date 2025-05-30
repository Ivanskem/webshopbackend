from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import current_user, login_required
from app.extensions import db
from app.models.product import Product
from app.models.order import Order, OrderItem
import json

bp = Blueprint('cart', __name__)

@bp.route('/')
@login_required
def view_cart():
 
    cart = session.get('cart', {})
    
    
    cart_items = []
    total = 0
    
    for product_id, item in cart.items():
        product = Product.query.get(product_id)
        if product:
            item_total = product.price * item['quantity']
            cart_items.append({
                'product': product,
                'quantity': item['quantity'],
                'total': item_total
            })
            total += item_total
    
    return render_template('cart/view.html', cart_items=cart_items, total=total)

@bp.route('/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    quantity = int(request.form.get('quantity', 1))
    
    cart = session.get('cart', {})
    
    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += quantity
    else:
        cart[str(product_id)] = {'quantity': quantity}
    
    session['cart'] = cart
    flash(f'"{product.name}" добавлен в корзину', 'success')
    return redirect(url_for('products.product_detail', product_id=product_id))

@bp.route('/update/<int:product_id>', methods=['POST'])
@login_required
def update_cart(product_id):
    quantity = int(request.form.get('quantity', 1))
    
    cart = session.get('cart', {})
    
    if str(product_id) in cart:
        if quantity > 0:
            cart[str(product_id)]['quantity'] = quantity
        else:
            del cart[str(product_id)]
    
    session['cart'] = cart
    return jsonify(success=True)

@bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    if request.method == 'POST':
        cart = session.get('cart', {})
        
        if not cart:
            flash('Ваша корзина пуста', 'warning')
            return redirect(url_for('cart.view_cart'))
        
     
        total = 0
        order = Order(user_id=current_user.id)
        db.session.add(order)
        db.session.commit()
        
      
        for product_id, item in cart.items():
            product = Product.query.get(product_id)
            if product and product.stock >= item['quantity']:
                total += product.price * item['quantity']
                
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=product_id,
                    quantity=item['quantity'],
                    price=product.price
                )
                db.session.add(order_item)
                
               
                product.stock -= item['quantity']
            else:
                db.session.rollback()
                flash('Недостаточно товара в наличии', 'danger')
                return redirect(url_for('cart.view_cart'))
        
       
        order.total = total
        db.session.commit()
       
        session.pop('cart', None)
        
        flash('Заказ успешно оформлен!', 'success')
        return redirect(url_for('main.index'))
    
    return render_template('cart/checkout.html')