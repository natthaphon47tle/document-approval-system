import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:

    SECRET_KEY = os.environ.get("SECRET_KEY", "das-secret-key")

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///" + os.path.join(BASE_DIR, "database", "database.db")
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True

    MAIL_USERNAME = "natthaphontle47@gmail.com"
    MAIL_PASSWORD = "fayt azse avek ppth"

    MAIL_DEFAULT_SENDER = MAIL_USERNAME

    ACCOUNTING_EMAIL = "natthaphon@leogloballogistics.com"