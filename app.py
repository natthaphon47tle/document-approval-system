import os

from flask import Flask
from config import Config
from extensions import db, login_manager

app = Flask(__name__)

app.config.from_object(Config)

app.config["UPLOAD_FOLDER"] = "uploads"

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

db.init_app(app)

login_manager.init_app(app)
login_manager.login_view = "auth.login"

from models.user import User
from models.document import Document
from models.approval import ApprovalHistory
from routes.document import document_bp
from services.email_service import send_test_email
from routes.dashboard import dashboard_bp
from routes.account import account_bp
from models.approval_step import ApprovalStep
from models.attachment import Attachment
from models.email_setting import EmailSetting
from routes.settings import settings_bp

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
from routes.auth import auth_bp
from routes.user import user_bp
app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(document_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(account_bp)
app.register_blueprint(settings_bp)

with app.app_context():
    db.create_all()

    from models.email_setting import EmailSetting

    if EmailSetting.query.count() == 0:
        setting = EmailSetting(
            recipient_email="accounting@gmail.com"
        )

        db.session.add(setting)
        db.session.commit()

        print("Email Setting Created")

@app.route("/test-email")
def test_email():

    send_test_email()

    return "EMAIL TEST SUCCESS"

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )