from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash


# create a blueprint object named auth and assign it to the __name__ variable
auth = Blueprint("auth", __name__) 


# create a route for the login page
@auth.route("/login", methods=['GET', 'POST'])
def login():
    # if request method is POST
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        # Get user from database using email
        user = User.query.filter_by(email=email).first()
        # if user exists
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in!", category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Password is incorrect.', category='error')
        else:
            flash('Email does not exist.', category='error')
    # Render the login page with User as the template context
    return render_template("login.html", user=current_user)

# create a route for the register page
@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    # if request method is POST
    if request.method == 'POST':
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        # Check if email already exists
        email_exists = User.query.filter_by(email=email).first()
        # Check if username already exists
        username_exists = User.query.filter_by(username=username).first()

        # if email already exists
        if email_exists:
            flash('Email is already in use.', category='error')
        # if username already exists
        elif username_exists:
            flash('Username is already in use.', category='error')
        # if passwords don't match
        elif password1 != password2:
            flash('Password don\'t match!', category='error')
        # if username length is less than 2
        elif len(username) < 2:
            flash('Username is too short.', category='error')
        # if password length is less than 6
        elif len(password1) < 6:
            flash('Password is too short.', category='error')
        # if email length is less than 4
        elif len(email) < 4:
            flash("Email is invalid.", category='error')
        # if all the conditions are met
        else:
            # create a new user
            new_user = User(email=email, username=username, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!')
            return redirect(url_for('views.home'))
    # Render the register page with User as the template context
    return render_template("signup.html", user=current_user)


# create a route for the logout page
@auth.route("/logout")
@login_required
def logout():
    # 
    logout_user()
    return redirect(url_for("views.home"))
