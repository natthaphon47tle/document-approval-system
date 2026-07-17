from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash

from extensions import db
from models.user import User

from flask import abort

user_bp = Blueprint("user", __name__)

@user_bp.route("/users")
@login_required
def users():

    if current_user.role != "Admin":
        abort(403)

    users = User.query.all()

    return render_template(
        "users/list.html",
        users=users
    )

@user_bp.route("/users/add", methods=["POST"])
@login_required
def add_user():

    if current_user.role != "Admin":
        abort(403)

    employee_id = request.form["employee_id"]
    fullname = request.form["fullname"]
    department = request.form["department"]
    position = request.form["position"]
    role = request.form["role"]
    status = request.form["status"]
    password = request.form["password"]
    confirm_password = request.form["confirm_password"]

    if password != confirm_password:
        return "Password ไม่ตรงกัน"

    new_user = User(
        employee_id=employee_id,
        fullname=fullname,
        username=employee_id,
        password=generate_password_hash(password),
        department=department,
        position=position,
        role=role,
        status=status
    )

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")