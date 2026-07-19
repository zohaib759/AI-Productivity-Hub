from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from flask import request
from app import db
from app.tasks import tasks
from app.tasks.forms import TaskForm
from app.models.task import Task


@tasks.route("/tasks")
@login_required
def all_tasks():

    search = request.args.get("search", "")
    priority = request.args.get("priority", "All")
    status = request.args.get("status", "All")

    query = Task.query.filter_by(user_id=current_user.id)

    # Search
    if search:
        query = query.filter(Task.title.ilike(f"%{search}%"))

    # Priority
    if priority != "All":
        query = query.filter(Task.priority == priority)

    # Status
    if status == "Completed":
        query = query.filter(Task.completed == True)

    elif status == "Pending":
        query = query.filter(Task.completed == False)

    tasks = query.order_by(
        Task.completed,
        Task.due_date,
        Task.due_time
    ).all()

    return render_template(
        "tasks.html",
        tasks=tasks,
        search=search,
        priority=priority,
        status=status
    )


@tasks.route("/tasks/create", methods=["GET", "POST"])
@login_required
def create_task():

    form = TaskForm()

    if form.validate_on_submit():

        task = Task(
            title=form.title.data,
            description=form.description.data,
            priority=form.priority.data,
            due_date=form.due_date.data,
            due_time=form.due_time.data,
            user_id=current_user.id
        )

        db.session.add(task)
        db.session.commit()

        flash("Task created successfully!", "success")

        return redirect(url_for("tasks.all_tasks"))

    return render_template(
        "create_task.html",
        form=form
    )


@tasks.route("/tasks/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_task(id):

    task = Task.query.get_or_404(id)

    if task.user_id != current_user.id:
        flash("Unauthorized!", "danger")
        return redirect(url_for("tasks.all_tasks"))

    form = TaskForm(obj=task)

    if form.validate_on_submit():

        task.title = form.title.data
        task.description = form.description.data
        task.priority = form.priority.data
        task.due_date = form.due_date.data
        task.due_time = form.due_time.data

        db.session.commit()

        flash("Task updated successfully!", "success")

        return redirect(url_for("tasks.all_tasks"))

    return render_template(
        "create_task.html",
        form=form,
        edit=True
    )


@tasks.route("/tasks/delete/<int:id>")
@login_required
def delete_task(id):

    task = Task.query.get_or_404(id)

    if task.user_id != current_user.id:
        flash("Unauthorized!", "danger")
        return redirect(url_for("tasks.all_tasks"))

    db.session.delete(task)
    db.session.commit()

    flash("Task deleted successfully!", "success")

    return redirect(url_for("tasks.all_tasks"))


@tasks.route("/tasks/complete/<int:id>")
@login_required
def complete_task(id):

    task = Task.query.get_or_404(id)

    if task.user_id != current_user.id:
        flash("Unauthorized!", "danger")
        return redirect(url_for("tasks.all_tasks"))

    task.completed = not task.completed

    db.session.commit()

    flash("Task status updated!", "success")

    return redirect(url_for("tasks.all_tasks"))