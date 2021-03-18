from flask import Blueprint, render_template, request, redirect, flash, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db 
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/sign-up', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        email = request.form["email"]
        fname = request.form["fname"]
        pass0 = request.form["password"]
        pass1 = request.form["password1"]
       
        user = User.query.filter_by(email = email).first()
        if user:
            flash("user already exists",category="error")
        elif pass0 != pass1:
            flash("password and confirm password is not same", category="error")
        else:
            new_user = User(email=email, fname=fname,
                            password=generate_password_hash(pass1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            # login_user(user,remember = True)
            flash("Accounte created", category="success")
            return redirect('/')

    return render_template("sign-up.html",user = current_user)


@auth.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email = email).first()
        if user:
            if check_password_hash(user.password,password):
                flash("logged in Successfully",category = "success")
                login_user(user,remember = True)
                return redirect(url_for('views.home'))
            else:
                flash("incorrect password",category="error")
        else:
            flash("email not exist",category="error")

    return render_template("login.html",user = current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
