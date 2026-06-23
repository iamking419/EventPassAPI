from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.student import Student
from app.routers.deps import get_current_user

router = APIRouter()


@router.get("/")
def get_stats(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    total = db.query(Student).count()
    verified = db.query(Student).filter(Student.verified == True).count()
    pending = total - verified

    entry_rate = (verified / total * 100) if total > 0 else 0

    return {
        "issued": total,
        "verified": verified,
        "pending": pending,
        "entry_rate": round(entry_rate, 2)
    }