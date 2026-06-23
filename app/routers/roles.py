from fastapi import HTTPException

def admin_only(user: dict):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

def security_or_admin(user: dict):
    if user.get("role") not in ["admin", "security"]:
        raise HTTPException(status_code=403, detail="Access denied. Security or Admin only")