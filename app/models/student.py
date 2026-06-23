from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from app.core.database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)

    full_name = Column(String)
    student_id = Column(String, unique=True)
    age = Column(Integer)
    class_name = Column(String)
    gender = Column(String)
    phone = Column(String)

    image_url = Column(String)

    invitation_code = Column(String, unique=True, index=True)

    verified = Column(Boolean, default=False)
    verified_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)