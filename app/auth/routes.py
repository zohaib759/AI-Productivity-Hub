from flask import render_template, redirect, url_for, flash
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)
from flask_login import login_user, logout_user, login_required
from app.auth.forms import LoginForm
from app.auth import auth
from app.auth.forms import RegistrationForm
from app import db
from app.models.user import User

@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():

        # Find the user by email
        user = User.query.filter_by(email=form.email.data).first()

        # Check if user exists and password is correct
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)

            flash("Login successful!", "success")

            return redirect(url_for("dashboard.home"))

        flash("Invalid email or password.", "danger")

    return render_template("login.html", form=form)

@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():

        # Check if username already exists
        existing_username = User.query.filter_by(
            username=form.username.data
        ).first()

        if existing_username:
            flash("Username already exists.", "danger")
            return render_template("register.html", form=form)

        # Check if email already exists
        existing_email = User.query.filter_by(
            email=form.email.data
        ).first()

        if existing_email:
            flash("Email already registered.", "danger")
            return render_template("register.html", form=form)

        # Hash the password
        hashed_password = generate_password_hash(form.password.data)

        # Create the user
        user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=hashed_password
        )

        # Save to database
        db.session.add(user)
        db.session.commit()

        flash("Account created successfully!", "success")

        return redirect(url_for("auth.login"))

    return render_template("register.html", form=form)
@auth.route("/logout")
@login_required
def logout():

    
    # Implement logout functionality here
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))