from models.approval_step import ApprovalStep


def can_view_document(document, user):

    # Admin ดูได้ทุกเอกสาร
    if user.role == "Admin":
        return True

    # เจ้าของเอกสาร
    if document.created_by == user.employee_id:
        return True

    # อยู่ใน Workflow
    step = ApprovalStep.query.filter_by(
        document_id=document.id,
        approver_id=user.id
    ).first()

    if step:
        return True

    return False