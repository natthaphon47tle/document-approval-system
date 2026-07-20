from datetime import datetime

from extensions import db
from models.document import Document
from models.approval_step import ApprovalStep
from models.approval import ApprovalHistory

def approve(document_id, user, comment):

    # ==============================
    # 1. หาเอกสาร
    # ==============================

    document = Document.query.get(document_id)

    if not document:
        return False, "Document not found."



    # ==============================
    # 2. หา Step ที่ผู้ใช้คนนี้ต้องอนุมัติ
    # ==============================

    current_step = ApprovalStep.query.filter_by(
        document_id=document.id,
        approver_id=user.id,
        status="Waiting"
    ).first()

    # ถ้าไม่ใช่คิวของตัวเอง
    if not current_step:
        return False, "You are not allowed to approve this document."



    # ==============================
    # 3. อนุมัติ Step ปัจจุบัน
    # ==============================

    current_step.status = "Approved"

    current_step.comment = comment

    current_step.approved_at = datetime.now()

    history = ApprovalHistory(
        document_id=document.id,
        approver=user.fullname,
        action="Approved",
        comment=comment
    )

    db.session.add(history)



    # ==============================
    # 4. หา Step ถัดไป
    # ==============================

    next_step = ApprovalStep.query.filter_by(
        document_id=document.id,
        sequence=current_step.sequence + 1
    ).first()



    # ==============================
    # 5. ถ้ามี Step ถัดไป
    # ==============================

    if next_step:

        # เปิดให้คนถัดไปอนุมัติ

        next_step.status = "Waiting"

        # เปลี่ยน Current Approver

        document.current_approver = str(next_step.approver_id)



    # ==============================
    # 6. ถ้าไม่มี Step ถัดไป
    # ==============================

    else:

        # Workflow เสร็จแล้ว

        document.status = "Approved"

        document.current_approver = None



    # ==============================
    # 7. บันทึกลงฐานข้อมูล
    # ==============================

    db.session.commit()



    # ==============================
    # 8. ส่งค่ากลับ
    # ==============================

    return True, "Document approved successfully."

def reject(document_id, user, comment):

    # ==============================
    # 1. หาเอกสาร
    # ==============================

    document = Document.query.get(document_id)

    if not document:
        return False, "Document not found."

    # ==============================
    # 2. หา Step ที่กำลัง Waiting
    # ==============================

    current_step = ApprovalStep.query.filter_by(
        document_id=document.id,
        approver_id=user.id,
        status="Waiting"
    ).first()

    if not current_step:
        return False, "You are not allowed to reject this document."

    # ==============================
    # 3. ต้องมี Comment
    # ==============================

    if not comment or comment.strip() == "":
        return False, "กรุณากรอกเหตุผลก่อน Reject"

    # ==============================
    # 4. เปลี่ยนสถานะ Step
    # ==============================

    current_step.status = "Rejected"
    current_step.comment = comment
    current_step.approved_at = datetime.now()

    history = ApprovalHistory(
        document_id=document.id,
        approver=user.fullname,
        action="Rejected",
        comment=comment
    )

    db.session.add(history)

    # ==============================
    # 5. จบ Workflow
    # ==============================

    document.status = "Rejected"
    document.current_approver = None

    # ==============================
    # 6. บันทึก
    # ==============================

    db.session.commit()

    # ==============================
    # 7. ส่งค่ากลับ
    # ==============================

    return True, "Document rejected successfully."