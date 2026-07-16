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

@notes.route("/notes/edit/<int:id>",methods=["GET","POST"])
@login_required
def edit_note(id):
    note = Note.query.get_or_404(id)

    if note.user_id != current_user.id:
        flash("You are not authorized to edit this note.", "danger")
        return redirect(url_for("notes.all_notes"))

    form = NoteForm(obj=note)

    if form.validate_on_submit():
        note.title = form.title.data
        note.content = form.content.data

        db.session.commit()

        flash("Note updated successfully!", "success")

        return redirect(url_for("notes.all_notes"))

    return render_template(
        "create_note.html",
        form=form,
        note=note
    )
@notes.route("/notes/delete/<int:id>")
@login_required
def delete_note(id):

    note = Note.query.get_or_404(id)

    if note.user_id != current_user.id:
        flash("You are not authorized to delete this note.", "danger")
        return redirect(url_for("notes.all_notes"))

    db.session.delete(note)
    db.session.commit()

    flash("Note deleted successfully!", "success")

    return redirect(url_for("notes.all_notes"))

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

