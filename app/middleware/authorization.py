from fastapi import HTTPException, status
from app.models.user import User

def is_admin(current_user: User) -> User:
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return current_user