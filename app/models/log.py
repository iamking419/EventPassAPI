from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from app.core.database import Base

class VerificationLog(Base):
    __tablename__ = "verification_logs"

    id = Column(Integer, primary_key=True)
    student_name = Column(String)
    code = Column(String)
    action = Column(String, default="GRANTED")  # CHECKED, GRANTED, REUSED, INVALID
    verified_by = Column(String)
    success = Column(Boolean, default=True)
    verified_at = Column(DateTime, default=datetime.utcnow)