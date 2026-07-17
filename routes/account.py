from flask import Blueprint, render_template
from flask_login import login_required, current_user

account_bp = Blueprint("account", __name__)


@account_bp.route("/account")
@login_required
def account():

    return render_template(
        "account/index.html",
        user=current_user
    )

from flask import request, flash, redirect
from werkzeug.security import check_password_hash, generate_password_hash
from extensions import db

@account_bp.route("/account/change-password", methods=["POST"])
@login_required
def change_password():

    current_password = request.form["current_password"]

    new_password = request.form["new_password"]

    confirm_password = request.form["confirm_password"]

    if not check_password_hash(
        current_user.password,
        current_password
    ):

        flash("Current password is incorrect.", "danger")

        return redirect("/account")

    if new_password != confirm_password:

        flash("New password does not match.", "warning")

        return redirect("/account")

    current_user.password = generate_password_hash(
        new_password
    )

    db.session.commit()

    flash("Password changed successfully.", "success")

    return redirect("/account")