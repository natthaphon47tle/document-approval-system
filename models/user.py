from extensions import db
from flask_login import UserMixin
from datetime import datetime


class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    employee_id = db.Column(db.String(20), unique=True, nullable=False)

    fullname = db.Column(db.String(200), nullable=False)

    username = db.Column(db.String(100), unique=True)

    password = db.Column(db.String(255), nullable=False)

    email = db.Column(db.String(150))

    department = db.Column(db.String(100))

    position = db.Column(db.String(100))

    role = db.Column(db.String(50), default="Employee")

    status = db.Column(db.String(20), default="Active")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    approval_steps = db.relationship(
        "ApprovalStep",
        backref="approver",
        lazy=True
    )