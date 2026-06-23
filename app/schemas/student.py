from pydantic import BaseModel
from typing import Optional

class StudentCreate(BaseModel):
    full_name: str
    student_id: str
    age: int
    class_name: str
    gender: str
    phone: Optional[str] = None