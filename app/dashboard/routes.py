from flask import render_template
from flask_login import login_required, current_user

from app.dashboard import dashboard
from app.models.note import Note
from app.models.task import Task

@dashboard.route("/dashboard")
@login_required
def home():

    total_notes = Note.query.filter_by(user_id=current_user.id).count()

    total_tasks = Task.query.filter_by(user_id=current_user.id).count()

    completed_tasks = Task.query.filter_by(
        user_id=current_user.id,
        completed=True
    ).count()

    pending_tasks = Task.query.filter_by(
        user_id=current_user.id,
        completed=False
    ).count()

    recent_notes = Note.query.filter_by(
        user_id=current_user.id
    ).order_by(Note.id.desc()).limit(5).all()

    recent_tasks = Task.query.filter_by(
        user_id=current_user.id
    ).order_by(Task.id.desc()).limit(5).all()

    return render_template(
        "dashboard.html",
        total_notes=total_notes,
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        pending_tasks=pending_tasks,
        recent_notes=recent_notes,
        recent_tasks=recent_tasks
    )