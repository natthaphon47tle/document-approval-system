from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash

from models.user import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        employee_id = request.form["employee_id"]
        password = request.form["password"]

        user = User.query.filter_by(employee_id=employee_id).first()

        if user and check_password_hash(user.password, password):

            login_user(user)

            return redirect("/dashboard")

        flash("Employee ID หรือ Password ไม่ถูกต้อง", "danger")

        return redirect("/")

    return render_template("auth/login.html")

@auth_bp.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect("/")