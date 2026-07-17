from datetime import datetime

from extensions import db


class ApprovalHistory(db.Model):

    __tablename__ = "approval_history"

    id = db.Column(db.Integer, primary_key=True)

    document_id = db.Column(
        db.Integer,
        db.ForeignKey("documents.id"),
        nullable=False
    )

    approver = db.Column(db.String(20), nullable=False)

    action = db.Column(db.String(20))

    comment = db.Column(db.Text)

    approved_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )