import os

from flask import Flask
from config import Config
from extensions import db, login_manager

app = Flask(__name__)

app.config.from_object(Config)

app.config["UPLOAD_FOLDER"] = "uploads"

db.init_app(app)

login_manager.init_app(app)
login_manager.login_view = "auth.login"

from models.user import User
from models.document import Document
from models.approval import ApprovalHistory
from routes.document import document_bp
from routes.dashboard import dashboard_bp
from routes.account import account_bp
from models.approval_step import ApprovalStep

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

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)