from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash
from app.extensions import db
from app.models.user import User
from app.utils.validators import validate_password, validate_email

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
    
        errors = []
        if User.query.filter_by(username=username).first():
            errors.append('Имя пользователя уже занято')
        if User.query.filter_by(email=email).first():
            errors.append('Email уже используется')
        
        email_valid, email_msg = validate_email(email)
        if not email_valid:
            errors.append(email_msg)
        
        password_valid, password_msg = validate_password(password)
        if not password_valid:
            errors.append(password_msg)
        
        if password != confirm_password:
            errors.append('Пароли не совпадают')
        
        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('auth/register.html')
        
     
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Регистрация прошла успешно! Теперь вы можете войти.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        remember = True if request.form.get('remember') else False
        
        user = User.query.filter_by(email=email).first()
        
        if not user or not user.check_password(password):
            flash('Неверный email или пароль', 'danger')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=remember)
        flash('Вход выполнен успешно!', 'success')
        return redirect(url_for('main.index'))
    
    return render_template('auth/login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы успешно вышли из системы', 'success')
    return redirect(url_for('main.index'))