from app import app, db
from flask import render_template, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from forms import LoginForm, RegisterForm
from models import User

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'signin'

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
            new_user = User(username=form.username.data, password=hash_password, email=form.email.data)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('signin'))
        else:
            return render_template('signup.html', form = form, info = "This username or email already used")
    return render_template('signup.html', form = form)

@app.route('/cats')
def cats():
    return "<h2>Cats here<h2>"

@app.route('/dogs')
def dogs():
    return "<h2>Dogs here<h2>"

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))