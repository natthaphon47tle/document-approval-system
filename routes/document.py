from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    current_app,
    send_from_directory,
    flash,
    abort
)
from flask_login import login_required, current_user

from datetime import datetime
from sqlalchemy import func

import os
from werkzeug.utils import secure_filename

from extensions import db
from models.document import Document
from models.user import User
from models.approval import ApprovalHistory
from models.approval_step import ApprovalStep
from services.permission_service import can_view_document
from services import approval_service
from flask import request, flash

document_bp = Blueprint("document", __name__)


@document_bp.route("/documents/create", methods=["GET", "POST"])
@login_required
def create_document():

    if request.method == "POST":

        today = datetime.now().strftime("%Y%m%d")

        document_type_code = request.form["document_type"]

        type_map = {
            "ASL_SUPPLIER_LIST": "Approve ASL Supplier List",
            "ASL_CASE": "Approve ASL Supplier Case by Case",
        }

        document_type = type_map.get(
            document_type_code,
            document_type_code
        )

        print(document_type)

        prefix_map = {
            "ASL_SUPPLIER_LIST": "ASL",
            "ASL_CASE": "ASLC",
        }

        prefix = prefix_map.get(
            document_type_code,
            "DOC"
        )

        count = Document.query.filter(
            func.date(Document.created_at) == datetime.today().date(),
            Document.document_no.like(f"{prefix}-%")
        ).count()

        document_no = f"{prefix}-{today}-{count+1:04d}"

        file = request.files.get("document_file")

        if not file or file.filename == "":

            flash(
                "Please select a document file.",
                "danger"
            )

            return redirect(
                url_for("document.create_document")
            )

        stored_filename = ""

        if file and file.filename != "":

            ext = os.path.splitext(file.filename)[1]

            stored_filename = secure_filename(
                document_no + ext
            )

            file.save(
                os.path.join(
                    current_app.config["UPLOAD_FOLDER"],
                    stored_filename
                )
            )

        document = Document(
            document_no=document_no,
            title=request.form["title"],
            document_type=request.form["document_type"],
            description=request.form["description"],
            file_name=stored_filename,
            created_by=current_user.employee_id
        )

        db.session.add(document)

        db.session.flush()

        approvers = request.form.getlist("approvers[]")

        for index, approver_id in enumerate(approvers, start=1):

            if not approver_id:
                continue

            approval = ApprovalStep(

                document_id=document.id,

                approver_id=int(approver_id),

                sequence=index,

                status="Waiting" if index == 1 else "Pending"

            )

            db.session.add(approval)

        db.session.commit()

        return redirect("/documents/create")

    users = User.query.filter_by(
        status="Active"
    ).order_by(User.fullname).all()

    return render_template(
        "documents/create.html",
        users=users
    )

@document_bp.route("/documents")
@login_required
def document_list():

    if current_user.role == "Admin":

        documents = Document.query.order_by(
            Document.created_at.desc()
        ).all()

    else:

        documents = Document.query.filter_by(
            created_by=current_user.employee_id
        ).order_by(
            Document.created_at.desc()
        ).all()

    return render_template(
        "documents/list.html",
        documents=documents
    )

@document_bp.route("/documents/view/<filename>")
@login_required
def view_document(filename):

    return send_from_directory(

        current_app.config["UPLOAD_FOLDER"],

        filename

    )

@document_bp.route("/documents/download/<filename>")
@login_required
def download_document(filename):

    return send_from_directory(

        current_app.config["UPLOAD_FOLDER"],

        filename,

        as_attachment=True

    )

@document_bp.route("/documents/<int:id>")
@login_required
def document_detail(id):

    document = Document.query.get_or_404(id)

    if not can_view_document(document, current_user):

        flash(
            "คุณไม่มีสิทธิ์เข้าถึงเอกสารนี้",
            "warning"
        )

        return redirect("/dashboard")

    current_step = ApprovalStep.query.filter_by(
        document_id=document.id,
        approver_id=current_user.id,
        status="Waiting"
    ).first()

    history = ApprovalHistory.query.filter_by(
        document_id=document.id
    ).order_by(
        ApprovalHistory.approved_at.asc()
    ).all()

    return render_template(
        "documents/detail.html",
        document=document,
        current_step=current_step,
        history=history
    )

@document_bp.route("/documents/waiting")
@login_required
def waiting_documents():

    waiting_steps = (
        ApprovalStep.query
        .filter_by(
            approver_id=current_user.id,
            status="Waiting"
        )
        .all()
    )

    return render_template(
        "documents/waiting.html",
        waiting_steps=waiting_steps
    )
    

@document_bp.route("/documents/reject/<int:id>", methods=["POST"])
@login_required
def reject_document(id):

    success, message = approval_service.reject(
        document_id=id,
        user=current_user,
        comment=request.form.get("comment")
    )

    flash(
        message,
        "success" if success else "danger"
    )

    return redirect(f"/documents/{id}")  

@document_bp.route("/history")
@login_required
def approval_history():

    histories = ApprovalHistory.query.order_by(
        ApprovalHistory.approved_at.desc()
    ).all()

    return render_template(
        "documents/history.html",
        histories=histories
    )

@document_bp.route("/documents/approve/<int:id>", methods=["POST"])
@login_required
def approve_document(id):

    success, message = approval_service.approve(
        document_id=id,
        user=current_user,
        comment=request.form.get("comment")
    )

    flash(
        message,
        "success" if success else "danger"
    )

    return redirect(f"/documents/{id}") 