from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.student import Student
from app.utils.code_generator import generate_code
from app.utils.files import save_image
from app.routers.deps import get_current_user
from app.routers.roles import admin_only, security_or_admin

router = APIRouter()


# -----------------------------
# 1. CREATE STUDENT — ADMIN ONLY
# -----------------------------
@router.post("/")
def create_student(
    full_name: str = Form(...),
    student_id: str = Form(...),
    age: int = Form(...),
    class_name: str = Form(...),
    gender: str = Form(...),
    phone: str = Form(None),
    image: UploadFile = File(...),

    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    admin_only(user)  # ✅ ADMIN ONLY

    image_path = save_image(image)
    code = generate_code()

    student = Student(
        full_name=full_name,
        student_id=student_id,
        age=age,
        class_name=class_name,
        gender=gender,
        phone=phone,
        image_url=image_path,
        invitation_code=code,
        verified=False
    )

    db.add(student)
    db.commit()
    db.refresh(student)

    return {
        "message": "Student created",
        "invitation_code": code,
        "student_id": student.id
    }


# -----------------------------
# 2. GET ALL STUDENTS — ADMIN + SECURITY
# -----------------------------
@router.get("/")
def get_students(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    security_or_admin(user)  # ✅ BOTH CAN VIEW

    students = db.query(Student).all()

    return [
        {
            "id": s.id,
            "full_name": s.full_name,
            "student_id": s.student_id,
            "age": s.age,
            "class_name": s.class_name,
            "gender": s.gender,
            "phone": s.phone,
            "image_url": s.image_url,
            "invitation_code": s.invitation_code,
            "verified": s.verified,
            "verified_at": s.verified_at.isoformat() if s.verified_at else None,
            "created_at": s.created_at.isoformat() if s.created_at else None,
            "status": "verified" if s.verified else "pending"
        }
        for s in students
    ]


# -----------------------------
# 3. DASHBOARD — ADMIN + SECURITY
# -----------------------------
@router.get("/dashboard")
def get_dashboard(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    security_or_admin(user)  # ✅ BOTH CAN VIEW

    students = db.query(Student).all()

    formatted = [
        {
            "id": s.id,
            "full_name": s.full_name,
            "student_id": s.student_id,
            "class_name": s.class_name,
            "age": s.age,
            "gender": s.gender,
            "phone": s.phone,
            "image_url": s.image_url,
            "invitation_code": s.invitation_code,
            "verified": s.verified,
            "verified_at": s.verified_at.isoformat() if s.verified_at else None,
            "created_at": s.created_at.isoformat() if s.created_at else None,
            "status": "verified" if s.verified else "pending"
        }
        for s in students
    ]

    verified_list = [s for s in formatted if s["verified"]]
    pending_list = [s for s in formatted if not s["verified"]]

    return {
        "all": formatted,
        "verified": verified_list,
        "pending": pending_list,
        "summary": {
            "total": len(formatted),
            "verified": len(verified_list),
            "pending": len(pending_list),
            "entry_rate": round(
                (len(verified_list) / len(formatted) * 100) if formatted else 0,
                2
            )
        }
    }


# -----------------------------
# 4. GET STUDENT BY INVITATION CODE — ADMIN + SECURITY
# -----------------------------
@router.get("/by-code/{code}")
def get_student_by_code(
    code: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    security_or_admin(user)  # ✅ BOTH CAN VIEW

    student = db.query(Student).filter(Student.invitation_code == code).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    return {
        "id": student.id,
        "full_name": student.full_name,
        "student_id": student.student_id,
        "age": student.age,
        "class_name": student.class_name,
        "gender": student.gender,
        "phone": student.phone,
        "image_url": student.image_url,
        "invitation_code": student.invitation_code,
        "verified": student.verified,
        "verified_at": student.verified_at.isoformat() if student.verified_at else None,
        "created_at": student.created_at.isoformat() if student.created_at else None,
        "status": "verified" if student.verified else "pending"
    }


# -----------------------------
# 5. GET SINGLE STUDENT — ADMIN + SECURITY
# -----------------------------
@router.get("/{student_id}")
def get_student(
    student_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    security_or_admin(user)  # ✅ BOTH CAN VIEW

    student = db.query(Student).filter(Student.id == student_id).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    return {
        "id": student.id,
        "full_name": student.full_name,
        "student_id": student.student_id,
        "age": student.age,
        "class_name": student.class_name,
        "gender": student.gender,
        "phone": student.phone,
        "image_url": student.image_url,
        "invitation_code": student.invitation_code,
        "verified": student.verified,
        "verified_at": student.verified_at.isoformat() if student.verified_at else None,
        "created_at": student.created_at.isoformat() if student.created_at else None,
        "status": "verified" if student.verified else "pending"
    }


# -----------------------------
# 6. UPDATE STUDENT — ADMIN ONLY
# -----------------------------
@router.put("/{student_id}")
def update_student(
    student_id: int,
    student_data: dict,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    admin_only(user)  # ✅ ADMIN ONLY

    student = db.query(Student).filter(Student.id == student_id).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    for field, value in student_data.items():
        if hasattr(student, field):
            setattr(student, field, value)

    db.commit()
    db.refresh(student)

    return {
        "id": student.id,
        "full_name": student.full_name,
        "student_id": student.student_id,
        "class_name": student.class_name,
        "verified": student.verified,
        "status": "verified" if student.verified else "pending"
    }


# -----------------------------
# 7. DELETE STUDENT — ADMIN ONLY
# -----------------------------
@router.delete("/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    admin_only(user)  # ✅ ADMIN ONLY

    student = db.query(Student).filter(Student.id == student_id).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    db.delete(student)
    db.commit()

    return {"message": "Student deleted successfully"}