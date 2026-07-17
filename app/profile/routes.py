from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from app.profile import profile
from app.profile.form import ProfileForm
from app import db
from app.models.user import User


@profile.route("/profile")
@login_required
def my_profile():
    return render_template(
        "profile.html",
        user=current_user
    )


@profile.route("/profile/edit", methods=["GET", "POST"])
@login_required
def edit_profile():

    form = ProfileForm()

    # Pre-fill the form when opening the page
    if form.username.data is None:
        form.username.data = current_user.username
        form.email.data = current_user.email

    if form.validate_on_submit():

        # Check if username already exists
        existing_username = User.query.filter(
            User.username == form.username.data,
            User.id != current_user.id
        ).first()

        if existing_username:
            flash("Username already exists.", "danger")
            return render_template(
                "edit_profile.html",
                form=form
            )

        # Check if email already exists
        existing_email = User.query.filter(
            User.email == form.email.data,
            User.id != current_user.id
        ).first()

        if existing_email:
            flash("Email already exists.", "danger")
            return render_template(
                "edit_profile.html",
                form=form
            )

        # Update profile
        current_user.username = form.username.data
        current_user.email = form.email.data

        db.session.commit()

        flash("Profile updated successfully!", "success")

        return redirect(url_for("profile.my_profile"))

    return render_template(
        "edit_profile.html",
        form=form
    )