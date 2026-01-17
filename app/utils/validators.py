import re
from fastapi import HTTPException, status

def validate_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password: str) -> None:
    if len(password) < 8:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password must be at least 8 characters")
    if not re.search(r'[A-Z]', password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password must contain uppercase")
    if not re.search(r'[a-z]', password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password must contain lowercase")
    if not re.search(r'\d', password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password must contain number")