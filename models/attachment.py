from datetime import datetime, timedelta

from extensions import db


class Attachment(db.Model):

    __tablename__ = "attachments"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    document_id = db.Column(
        db.Integer,
        db.ForeignKey("documents.id"),
        nullable=False
    )

    file_name = db.Column(
        db.String(255),
        nullable=False
    )

    file_path = db.Column(
        db.String(255),
        nullable=False
    )

    uploaded_at = db.Column(
        db.DateTime,
        default=lambda: datetime.utcnow() + timedelta(hours=7)
    )