from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.database import get_db
from src.models import User
from src.oauth2 import create_access_token
from src.schemas import Token
from src.utils import verify_password

router = APIRouter(prefix="/login", tags=["Authentication Endpoint"])


@router.post("/", response_model=Token)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> Token:
    """
    The function creates an `access_token` for the authenticated user.
    """
    user = (
        db.query(User).filter(User.email == user_credentials.username).first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials.",
        )

    if not verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials.",
        )

    access_token = create_access_token(payload={"user_id": user.user_id})

    return Token(access_token=access_token, token_type="bearer")
