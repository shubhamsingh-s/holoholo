from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///holoholo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), default='customer')  # customer or admin
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    orders = db.relationship('Order', backref='user', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    products = db.relationship('Product', backref='category', lazy=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    image_url = db.Column(db.String(200))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviews = db.relationship('Review', backref='product', lazy=True)
    order_items = db.relationship('OrderItem', backref='product', lazy=True)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='pending')
    shipping_address = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    items = db.relationship('OrderItem', backref='order', lazy=True)

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def home():
    featured_products = Product.query.limit(8).all()
    categories = Category.query.all()
    return render_template('home.html', products=featured_products, categories=categories)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return render_template('signup.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return render_template('signup.html')
        
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('home'))

@app.route('/products')
def products():
    category_id = request.args.get('category', type=int)
    sort_by = request.args.get('sort', 'name')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    
    query = Product.query
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
    
    if sort_by == 'price_low':
        query = query.order_by(Product.price.asc())
    elif sort_by == 'price_high':
        query = query.order_by(Product.price.desc())
    elif sort_by == 'name':
        query = query.order_by(Product.name.asc())
    elif sort_by == 'newest':
        query = query.order_by(Product.created_at.desc())
    
    products = query.all()
    categories = Category.query.all()
    
    return render_template('products.html', products=products, categories=categories)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    reviews = Review.query.filter_by(product_id=product_id).order_by(Review.created_at.desc()).all()
    return render_template('product_detail.html', product=product, reviews=reviews)

@app.route('/add_to_cart', methods=['POST'])
@login_required
def add_to_cart():
    product_id = request.form.get('product_id')
    quantity = int(request.form.get('quantity', 1))
    
    if 'cart' not in session:
        session['cart'] = {}
    
    if product_id in session['cart']:
        session['cart'][product_id] += quantity
    else:
        session['cart'][product_id] = quantity
    
    session.modified = True
    flash('Product added to cart!', 'success')
    return redirect(request.referrer)

@app.route('/cart')
@login_required
def cart():
    if 'cart' not in session or not session['cart']:
        return render_template('cart.html', cart_items=[], total=0)
    
    cart_items = []
    total = 0
    
    for product_id, quantity in session['cart'].items():
        product = Product.query.get(product_id)
        if product:
            item_total = product.price * quantity
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total': item_total
            })
            total += item_total
    
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/update_cart', methods=['POST'])
@login_required
def update_cart():
    product_id = request.form.get('product_id')
    quantity = int(request.form.get('quantity', 0))
    
    if quantity <= 0:
        session['cart'].pop(product_id, None)
    else:
        session['cart'][product_id] = quantity
    
    session.modified = True
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    if request.method == 'POST':
        shipping_address = request.form.get('shipping_address')
        
        if 'cart' not in session or not session['cart']:
            flash('Your cart is empty', 'error')
            return redirect(url_for('cart'))
        
        total_amount = 0
        order_items = []
        
        for product_id, quantity in session['cart'].items():
            product = Product.query.get(product_id)
            if product and product.stock >= quantity:
                total_amount += product.price * quantity
                order_items.append({
                    'product': product,
                    'quantity': quantity,
                    'price': product.price
                })
        
        if not order_items:
            flash('No valid items in cart', 'error')
            return redirect(url_for('cart'))
        
        # Create order
        order = Order(
            user_id=current_user.id,
            total_amount=total_amount,
            shipping_address=shipping_address
        )
        db.session.add(order)
        db.session.flush()
        
        # Create order items
        for item in order_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item['product'].id,
                quantity=item['quantity'],
                price=item['price']
            )
            db.session.add(order_item)
            
            # Update stock
            item['product'].stock -= item['quantity']
        
        db.session.commit()
        
        # Clear cart
        session.pop('cart', None)
        
        flash('Order placed successfully!', 'success')
        return redirect(url_for('order_history'))
    
    return render_template('checkout.html')

@app.route('/order_history')
@login_required
def order_history():
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('order_history.html', orders=orders)

@app.route('/add_review', methods=['POST'])
@login_required
def add_review():
    product_id = request.form.get('product_id')
    rating = int(request.form.get('rating'))
    comment = request.form.get('comment')
    
    review = Review(
        user_id=current_user.id,
        product_id=product_id,
        rating=rating,
        comment=comment
    )
    db.session.add(review)
    db.session.commit()
    
    flash('Review added successfully!', 'success')
    return redirect(url_for('product_detail', product_id=product_id))

@app.route('/search')
def search():
    query = request.args.get('q', '')
    if query:
        products = Product.query.filter(Product.name.contains(query)).all()
    else:
        products = []
    
    return render_template('search_results.html', products=products, query=query)

# Admin routes
@app.route('/admin')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('home'))
    
    total_products = Product.query.count()
    total_orders = Order.query.count()
    total_users = User.query.count()
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
    
    # Calculate total revenue
    total_revenue = db.session.query(db.func.sum(Order.total_amount)).scalar() or 0
    
    return render_template('admin/dashboard.html', 
                         total_products=total_products,
                         total_orders=total_orders,
                         total_users=total_users,
                         recent_orders=recent_orders,
                         total_revenue=total_revenue)

@app.route('/admin/products')
@login_required
def admin_products():
    if current_user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('home'))
    
    products = Product.query.all()
    categories = Category.query.all()
    return render_template('admin/products.html', products=products, categories=categories)

@app.route('/admin/add_product', methods=['GET', 'POST'])
@login_required
def admin_add_product():
    if current_user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = float(request.form.get('price'))
        stock = int(request.form.get('stock'))
        category_id = int(request.form.get('category_id'))
        
        product = Product(
            name=name,
            description=description,
            price=price,
            stock=stock,
            category_id=category_id
        )
        db.session.add(product)
        db.session.commit()
        
        flash('Product added successfully!', 'success')
        return redirect(url_for('admin_products'))
    
    categories = Category.query.all()
    return render_template('admin/add_product.html', categories=categories)

@app.route('/admin/orders')
@login_required
def admin_orders():
    if current_user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('home'))
    
    orders = Order.query.order_by(Order.created_at.desc()).all()
    total_revenue = db.session.query(db.func.sum(Order.total_amount)).scalar() or 0
    
    return render_template('admin/orders.html', orders=orders, total_revenue=total_revenue)

@app.route('/admin/users')
@login_required
def admin_users():
    if current_user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('home'))
    
    users = User.query.all()
    return render_template('admin/users.html', users=users)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Create admin user if not exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@holoholo.com',
                password_hash=generate_password_hash('admin123'),
                role='admin'
            )
            db.session.add(admin)
        
        # Create sample categories if not exist
        if Category.query.count() == 0:
            categories = [
                Category(name='Electronics', description='Electronic devices and gadgets'),
                Category(name='Clothing', description='Fashion and apparel'),
                Category(name='Books', description='Books and literature'),
                Category(name='Home & Garden', description='Home improvement and garden supplies'),
                Category(name='Sports', description='Sports equipment and accessories')
            ]
            for category in categories:
                db.session.add(category)
        
        # Create sample products if not exist
        if Product.query.count() == 0:
            products = [
                Product(name='Smartphone X', description='Latest smartphone with advanced features', price=599.99, stock=50, category_id=1),
                Product(name='Laptop Pro', description='High-performance laptop for professionals', price=1299.99, stock=25, category_id=1),
                Product(name='Wireless Headphones', description='Premium wireless headphones with noise cancellation', price=199.99, stock=100, category_id=1),
                Product(name='Men\'s T-Shirt', description='Comfortable cotton t-shirt', price=24.99, stock=200, category_id=2),
                Product(name='Women\'s Dress', description='Elegant summer dress', price=89.99, stock=75, category_id=2),
                Product(name='Running Shoes', description='Professional running shoes', price=129.99, stock=60, category_id=5),
                Product(name='Garden Tool Set', description='Complete set of garden tools', price=79.99, stock=40, category_id=4),
                Product(name='Programming Book', description='Learn Python programming', price=39.99, stock=80, category_id=3)
            ]
            for product in products:
                db.session.add(product)
        
        db.session.commit()
    
    app.run(debug=True) 