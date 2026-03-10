"""
api/routes_auth.py
------------------
Authentication endpoints for civic officers.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.database import get_db
from db.models import Officer
from api.schemas import OfficerLogin, Token
from core.security import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=Token)
def login(
    credentials: OfficerLogin,
    db: Session = Depends(get_db),
):
    """
    Authenticate an officer and return a JWT access token.
    """
    officer = (
        db.query(Officer)
        .filter(Officer.username == credentials.username)
        .first()
    )

    if officer is None or not verify_password(credentials.password, officer.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(
        data={
            "sub": officer.username,
            "ward": officer.ward,
            "role": officer.role,
        }
    )

    return Token(access_token=token)
