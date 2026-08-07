from flask import Blueprint, render_template, request, flash, redirect
from extensions import db
from models.email_setting import EmailSetting

settings_bp = Blueprint("settings", __name__)   # ต้องอยู่ก่อน

@settings_bp.route("/settings", methods=["GET", "POST"])
def settings():

    email_setting = EmailSetting.query.first()

    if request.method == "POST":
        email_setting.recipient_email = request.form["recipient_email"]
        #email_setting.cc_email = request.form["cc_email"]

        db.session.commit()

        flash("Email settings updated successfully.", "success")

        return redirect("/settings")

    return render_template(
        "settings/index.html",
        email_setting=email_setting
    )