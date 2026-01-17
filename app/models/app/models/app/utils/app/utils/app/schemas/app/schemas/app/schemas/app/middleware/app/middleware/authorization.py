from fastapi import HTTPException, status
from app.models.user import User
from typing import List


def require_role(allowed_roles: List[str]):
    """
    Dependency to check if user has required role
    Usage: Depends(require_role(["admin"]))
    """
    def role_checker(current_user: User) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return current_user
    return role_checker


def is_admin(current_user: User) -> User:
    """Check if user is admin"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user