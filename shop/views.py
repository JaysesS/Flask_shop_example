from app import app, db
from flask import render_template, redirect, url_for, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView

from forms import LoginForm, RegisterForm
from models import User, Product, Order

from procedure import query_view_product

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'signin'

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

admin = Admin(app, index_view=AdminViewIndex())
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
    pq = Product.query.all()
    products = query_view_product(pq)
    return render_template('shop.html', products = products)

@app.route('/order', methods = ['POST'])
def order():
    order = request.get_json()
    print(order)
    return jsonify(success=True, data=order)

@app.route('/account')
def account():
    return render_template('account.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))