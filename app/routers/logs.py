from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.database import get_db
from app.models.log import VerificationLog
from app.routers.deps import get_current_user
from app.routers.roles import admin_only

router = APIRouter()


# -----------------------------
# 1. GET ALL LOGS (admin only)
# -----------------------------
@router.get("/")
def get_logs(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    admin_only(user)

    logs = db.query(VerificationLog).order_by(VerificationLog.verified_at.desc()).all()

    return [
        {
            "id": log.id,
            "student_name": log.student_name,
            "code": log.code,
            "verified_by": log.verified_by,
            "verified_at": log.verified_at.isoformat() if log.verified_at else None
        }
        for log in logs
    ]


# -----------------------------
# 2. GET LOGS BY SECURITY GUARD
# -----------------------------
@router.get("/by-guard/{guard_username}")
def get_logs_by_guard(
    guard_username: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    admin_only(user)

    logs = db.query(VerificationLog).filter(
        VerificationLog.verified_by == guard_username
    ).order_by(VerificationLog.verified_at.desc()).all()

    return [
        {
            "id": log.id,
            "student_name": log.student_name,
            "code": log.code,
            "verified_at": log.verified_at.isoformat() if log.verified_at else None
        }
        for log in logs
    ]


# -----------------------------
# 3. GET MY LOGS (security guard sees own activity)
# -----------------------------
@router.get("/me")
def get_my_logs(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    """Security guards can see their own verification history."""

    logs = db.query(VerificationLog).filter(
        VerificationLog.verified_by == user.get("username")
    ).order_by(VerificationLog.verified_at.desc()).all()

    return [
        {
            "id": log.id,
            "student_name": log.student_name,
            "code": log.code,
            "verified_at": log.verified_at.isoformat() if log.verified_at else None
        }
        for log in logs
    ]


# -----------------------------
# 4. GET LOG STATS
# -----------------------------
@router.get("/stats")
def get_log_stats(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    admin_only(user)

    total_checks = db.query(VerificationLog).count()
    total_granted = db.query(VerificationLog).filter(
        VerificationLog.student_name.isnot(None)
    ).count()

    # Top security guards by activity
    top_guards = db.query(
        VerificationLog.verified_by,
        func.count(VerificationLog.id).label("count")
    ).group_by(VerificationLog.verified_by).order_by(func.count(VerificationLog.id).desc()).limit(5).all()

    return {
        "total_checks": total_checks,
        "total_granted": total_granted,
        "top_guards": [
            {"username": guard[0], "verifications": guard[1]}
            for guard in top_guards
        ]
    }
    