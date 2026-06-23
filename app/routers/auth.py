from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import verify_password, create_access_token
from app.models.user import User
from app.schemas.auth import LoginSchema

router = APIRouter()


@router.post("/login")
def login(data: LoginSchema, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.username == data.username).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(
        data={"sub": user.username, "role": user.role}
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user.role
    }