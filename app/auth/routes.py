from flask import render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash

from app.auth import auth
from app.auth.forms import RegistrationForm
from app import db
from app.models.user import User

@auth.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")

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