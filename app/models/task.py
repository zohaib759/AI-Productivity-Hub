from app import db
from datetime import datetime

class Task(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=False)

    description = db.Column(db.Text)

    completed = db.Column(
        db.Boolean,
        default=False
    )

    priority = db.Column(
        db.String(20),
        default="Medium"
    )

    due_date = db.Column(db.Date)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )