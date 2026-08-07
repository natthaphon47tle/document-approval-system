from datetime import datetime
from extensions import db

class EmailSetting(db.Model):

    __tablename__ = "email_settings"

    id = db.Column(db.Integer, primary_key=True)

    recipient_email = db.Column(
        db.String(255),
        nullable=False
    )

    cc_email = db.Column(
        db.String(255),
        nullable=True
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )