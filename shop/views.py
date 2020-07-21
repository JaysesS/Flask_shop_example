from app import app, db
from flask import render_template, redirect, url_for, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask import session

from forms import LoginForm, RegisterForm, AccountForm
from models import User, Product, Order

from flask_nav import Nav
from nav import init_custom_nav_renderer, anon, auth, admin

from shop import view_products, get_product_dict, check_exist_product, update_amount_product, get_cost_cart, get_money_by_username, check_order, update_cost_cart, remove_product_cart

from account import get_user_info
from products import delete_all_products, fill_all_products 


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'signin'

nav = Nav(app)
nav.register_element('navbarAnon', anon)
nav.register_element('navbarAuth', auth)
nav.register_element('navbarAdmin', admin)
init_custom_nav_renderer(app)

class AdminViewModels(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated:
            if current_user.username == 'jayse' or \
                current_user.username == 'admin':
                return True
        else:
            return False
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('index'))

class AdminViewIndex(AdminIndexView):
    def is_accessible(self):
        if current_user.is_authenticated:
            if current_user.username == 'jayse' or \
                current_user.username == 'admin':
                return True
        else:
            return False
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('index'))

admin = Admin(app, index_view=AdminViewIndex(), endpoint='admin')
admin.add_view(AdminViewModels(User, db.session))
admin.add_view(AdminViewModels(Product, db.session))
admin.add_view(AdminViewModels(Order, db.session))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('index.html', name = current_user.username)
    return render_template('index.html', name = "Anonymous")

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.is_submitted():
        user = User.query.filter_by(username = form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            session['cart'] = []
            if user.phone == '' or user.adress == '':
                return redirect(url_for('account'))
            return redirect(url_for('index'))
        return render_template('signin.html', form = form, info = "Check input data")
    return render_template('signin.html', form = form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        email = User.query.filter_by(email = form.email.data).first()
        if user is None and email is None:
            hash_password = generate_password_hash(form.password.data, method='sha256')
            new_user = User(username = form.username.data, 
                            password = hash_password, 
                            email = form.email.data,
                            phone = '',
                            adress = '',
                            money = 0,
                            image = None)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('signin'))
        else:
            return render_template('signup.html', form = form, info = "This username or email already used")
    return render_template('signup.html', form = form)

@app.route('/shop/')
def shop():
    products = view_products()
    return render_template('shop.html', products = products)

@app.route('/api/delete_products')
@login_required
def delete_products():
    if current_user.username == "jayse" or current_user.username == "admin":
        delete_all_products()
        return jsonify(success=True)
    return jsonify(success=False)

@app.route('/api/fill_products')
@login_required
def fill_products():
    if current_user.username == "jayse" or current_user.username == "admin":
        delete_all_products()
        fill_all_products()
        return jsonify(success=True)
    return jsonify(success=False)

@app.route('/api/add_to_cart', methods = ['POST'])
@login_required
def add_to_cart():
    cart = session['cart']
    add_order = request.get_json()
    id = int(add_order['id'])
    amount = int(add_order['amount'])
    if check_exist_product(cart, id):
        cart = update_amount_product(cart, id, amount)
    else:
        product = get_product_dict(id)
        product["amount"] = amount
        cart.append(product)
    session['cart'] = cart
    return jsonify(success=True)

@app.route('/api/make_order', methods = ['POST'])
@login_required
def make_order():
    order = request.get_json()
    cart = session['cart']
    user_wallet = get_money_by_username(current_user.username)
    check = check_order(order, cart, user_wallet)
    user_info = get_user_info(current_user.username)
    if len(check) == 0:
        for item in cart:
            product = Product.query.filter_by(id = item['id']).first()
            user = User.query.filter_by(username = current_user.username).first()
            order = Order(
                username = current_user.username,
                email = user_info['email'],
                adress = user_info['adress'],
                phone = user_info['phone'],
                product = item['name'],
                category = item['category'],
                count = item['amount'])
            product.count -= item['amount']
            user.money -= product.price * item['amount']
            db.session.add(order)
            db.session.add(user)
            db.session.add(product)
            db.session.commit()
        session['cart'] = []
        return jsonify(info = 'Your order has been sent!', order=True, success=True)
    else:
        print('Some problem')
        return jsonify(info = check, order=False, success=True)

@app.route('/api/update_cost', methods = ['POST'])
@login_required
def update_cost():
    cart = session['cart']
    added = request.get_json()
    id = int(added['id'])
    amount = int(added['amount'])
    session['cart'] = update_cost_cart(cart, amount, id)
    new_cost = get_cost_cart(session['cart'])
    return jsonify(cost = new_cost, success=True)

@app.route('/api/get_cost', methods=['GET'])
@login_required
def get_cost():
    return jsonify(cost = get_cost_cart(session['cart']))

@app.route('/api/remove_item_cart', methods = ['POST'])
@login_required
def remove_item_cart():
    item_id = int(request.get_json()['id'])
    cart = session['cart']
    session['cart'] = remove_product_cart(cart, item_id)
    return jsonify(success=True)

@app.route('/cart')
@login_required
def cart():
    try:
        cart = session['cart']
    except KeyError:
        session['cart'] = list()
        cart = session['cart']
    cost = get_cost_cart(cart)
    user_wallet = get_money_by_username(current_user.username)
    return render_template('cart.html', cart = cart, cost = cost, user_wallet = user_wallet)

@app.route('/cart_clear', methods = ['POST', 'GET'])
@login_required
def cart_clear():
    session['cart'] = list()
    return redirect(url_for('cart'))

@app.route('/account', methods = ['POST', 'GET'])
@login_required
def account():
    user_info = get_user_info(current_user.username)
    form  = AccountForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = current_user.username).first()
        user.phone = form.phone.data
        user.adress = form.adress.data
        user.money = int(form.money.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('account'))
    return render_template('account.html', form = form, email = user_info['email'], money = user_info['money'], phone = user_info['phone'], adress = user_info['adress'])

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))