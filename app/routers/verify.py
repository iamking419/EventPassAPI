from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.database import get_db
from app.models.student import Student
from app.models.log import VerificationLog
from app.routers.deps import get_current_user
from app.routers.roles import security_or_admin

router = APIRouter()


# -----------------------------
# CHECK CODE (security can view)
# -----------------------------
@router.get("/{code}")
def check_code(
    code: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    security_or_admin(user)

    student = db.query(Student).filter(Student.invitation_code == code).first()

    if not student:
        return {
            "valid": False,
            "already_used": False,
            "student": None
        }

    return {
        "valid": True,
        "already_used": student.verified,
        "student": {
            "full_name": student.full_name,
            "student_id": student.student_id,
            "class_name": student.class_name,
            "age": student.age,
            "image_url": student.image_url
        }
    }


# -----------------------------
# VERIFY CODE (security can mark entry)
# -----------------------------
@router.post("/{code}")
def verify_code(
    code: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    security_or_admin(user)

    student = db.query(Student).filter(Student.invitation_code == code).first()

    if not student:
        raise HTTPException(status_code=404, detail="Invalid code")

    if student.verified:
        return {
            "success": False,
            "message": "Code already used",
            "student": {
                "full_name": student.full_name,
                "student_id": student.student_id,
                "class_name": student.class_name
            }
        }

    # Mark as verified
    student.verified = True
    student.verified_at = datetime.utcnow()
    db.commit()

    # Log the verification
    log = VerificationLog(
        student_name=student.full_name,
        code=code,
        verified_by=user.get("username"),
        verified_at=datetime.utcnow()
    )
    db.add(log)
    db.commit()

    return {
        "success": True,
        "message": "Entry Granted",
        "student": {
            "full_name": student.full_name,
            "student_id": student.student_id,
            "class_name": student.class_name
        }
    }