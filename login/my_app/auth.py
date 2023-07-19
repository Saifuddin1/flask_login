from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from my_app.database import db
from my_app.models import User
import re
import hashlib
from functools import wraps

auth_bp = Blueprint("auth_bp", __name__)


@auth_bp.route("/")
def index():
    return render_template("index.html", title="index")


@auth_bp.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form.get("fname")
        last_name = request.form.get("lname")
        email = request.form.get("email")
        password = hashlib.sha256(request.form.get(
            "password").encode()).hexdigest()

        is_user_exists = db.session.query(User).filter(
            User.email == email).first()
        if is_user_exists:
            flash('User Already Exists with provided email', 'warning')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address !', 'warning')
        else:
            user = User(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password
            )
            db.session.add(user)
            db.session.commit()
            flash('User Created Successfully', 'success')
    return render_template("user_signup.html", title="signup")


@auth_bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = hashlib.sha256(request.form.get(
            "password").encode()).hexdigest()
        account = db.session.query(User).filter(
            User.email == email).first()
        if account:
            if password == account.password:
                session['loggedin'] = True
                session['email'] = account.email
                flash('Logged in successfully !', 'success')
                return redirect(url_for('auth_bp.index'))
            else:
                flash('Incorrect Password !', 'danger')
        else:
            flash('Incorrect Email !', 'danger')
    return render_template("user_login.html", title="signup")


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth_bp.login'))


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not 'email' in session:
            return redirect(url_for('auth_bp.login'))
        return f(*args, **kwargs)
    return decorated_function


@auth_bp.route("/protected_page")
@login_required
def protected_page():
    return render_template("protected_page.html")
