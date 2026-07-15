from flask import render_template,redirect, url_for, flash
from flask_login import login_required,current_user

from app.notes import notes
from app.notes.form import NoteForm
from app.models.note import Note
from app import db


@notes.route('/notes')
@login_required
def all_notes():
    notes = Note.query.filter_by(user_id=current_user.id).all()
    return render_template('notes.html', notes=notes)

@notes.route("/notes/create", methods=["GET", "POST"])
@login_required
def create_note():

    form = NoteForm()

    if form.validate_on_submit():

        note = Note(
            title=form.title.data,
            content=form.content.data,
            user_id=current_user.id
        )

        db.session.add(note)
        db.session.commit()

        flash("Note created successfully!", "success")

        return redirect(url_for("notes.all_notes"))

    return render_template(
        "create_note.html",
        form=form
    )

