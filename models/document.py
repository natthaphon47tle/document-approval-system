from datetime import datetime

from extensions import db


class Document(db.Model):

    __tablename__ = "documents"

    id = db.Column(db.Integer, primary_key=True)

    document_no = db.Column(db.String(30), unique=True, nullable=False)

    title = db.Column(db.String(255), nullable=False)

    document_type = db.Column(db.String(100), nullable=False)

    description = db.Column(db.Text)

    file_name = db.Column(db.String(255))

    status = db.Column(db.String(50), default="Waiting Manager")

    created_by = db.Column(db.String(20))

    current_approver = db.Column(db.String(20))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    approval_steps = db.relationship(
        "ApprovalStep",
        backref="document",
        lazy=True,
        cascade="all, delete-orphan",
        order_by="ApprovalStep.sequence"
    )