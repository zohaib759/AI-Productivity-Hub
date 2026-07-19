from datetime import date
from flask import render_template
from flask_login import login_required, current_user

from app.dashboard import dashboard
from app.models.note import Note
from app.models.task import Task


@dashboard.route("/dashboard")
@login_required
def home():

    total_notes = Note.query.filter_by(
        user_id=current_user.id
    ).count()

    total_tasks = Task.query.filter_by(
        user_id=current_user.id
    ).count()

    completed_tasks = Task.query.filter_by(
        user_id=current_user.id,
        completed=True
    ).count()

    pending_tasks = Task.query.filter_by(
        user_id=current_user.id,
        completed=False
    ).count()

    today_tasks = Task.query.filter(
        Task.user_id == current_user.id,
        Task.completed == False,
        Task.due_date == date.today()
    ).order_by(Task.due_time).all()

    overdue_tasks = Task.query.filter(
        Task.user_id == current_user.id,
        Task.completed == False,
        Task.due_date < date.today()
    ).order_by(Task.due_date).all()

    recent_notes = (
        Note.query
        .filter_by(user_id=current_user.id)
        .order_by(Note.created_at.desc())
        .limit(5)
        .all()
    )

    return render_template(
        "dashboard.html",
        total_notes=total_notes,
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        pending_tasks=pending_tasks,
        today_tasks=today_tasks,
        overdue_tasks=overdue_tasks,
        recent_notes=recent_notes
    )