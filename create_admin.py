from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models.user import User

db = SessionLocal()

# Admin
admin = User(
    username="Admins",
    email="admins@school.com",
    password_hash=hash_password("admin@questland"),
    role="admin"
)

# Security Guard
guard = User(
    username="security",
    email="security@school.com",
    password_hash=hash_password("guard@questland"),
    role="security"
)

db.add(admin)
db.add(guard)
db.commit()

print("Admin and Security guard created")