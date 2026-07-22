from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models.user import User

db = SessionLocal()

# Admin
admin = User(
    username="admin",
    email="admin",
    password_hash=hash_password("admin"),
    role="admin"
)

# Security Guard
guard = User(
    username="security",
    email="security",
    password_hash=hash_password("security"),
    role="security"
)

db.add(admin)
db.add(guard)
db.commit()

print("Admin and Security guard created")