from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from models.approval_step import ApprovalStep

from models.document import Document

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
@login_required
def dashboard():

    search = request.args.get("search", "").strip()
    status = request.args.get("status", "").strip()

    total_documents = Document.query.count()

    waiting_documents = ApprovalStep.query.filter_by(
        approver_id=current_user.id,
        status="Waiting"
    ).count()

    approved_documents = Document.query.filter_by(
        status="Approved"
    ).count()

    rejected_documents = Document.query.filter_by(
        status="Rejected"
    ).count()

    if current_user.role == "Admin":

        recent_query = Document.query

    else:

        recent_query = Document.query.filter_by(
            created_by=current_user.employee_id
        )

    if search:
        recent_query = recent_query.filter(
            (Document.document_no.ilike(f"%{search}%")) |
            (Document.title.ilike(f"%{search}%"))
        )

    if status:
        recent_query = recent_query.filter(
            Document.status == status
        )

    recent_documents = (
        recent_query
        .order_by(Document.id.desc())
        .limit(5)
        .all()
    )

    waiting_query = ApprovalStep.query.filter_by(
        approver_id=current_user.id,
        status="Waiting"
    )

    if search:

        waiting_query = (
            waiting_query
            .join(Document)
            .filter(
                (Document.document_no.ilike(f"%{search}%")) |
                (Document.title.ilike(f"%{search}%"))
            )
        )

    waiting_approvals = (
        waiting_query
        .order_by(ApprovalStep.sequence)
        .limit(5)
        .all()
    )

    return render_template(
        "dashboard/index.html",

        total_documents=total_documents,

        waiting_approvals=waiting_approvals,

        waiting_documents=waiting_documents,

        approved_documents=approved_documents,

        rejected_documents=rejected_documents,

        recent_documents=recent_documents,

        search=search,

        status=status

    )