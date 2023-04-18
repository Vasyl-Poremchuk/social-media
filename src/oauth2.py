import json
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from src.config import settings
from src.database import get_db
from src.models import User
from src.schemas import TokenPayload

OAUTH2_SCHEMA = OAuth2PasswordBearer(tokenUrl="login")
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


def create_access_token(payload: dict) -> str:
    """
    The function creates an `access_token` for the authenticated user.
    """
    to_encode = payload.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire_str = expire.isoformat()
    expire_json = json.dumps(expire_str)
    to_encode.update({"expiration_time": expire_json})

    encoded_jwt = jwt.encode(
        claims=to_encode, key=SECRET_KEY, algorithm=ALGORITHM
    )

    return encoded_jwt


def verify_access_token(
    token: str, credentials_exception: HTTPException
) -> TokenPayload:
    """
    The creates a `payload` for the `access_token`.
    """
    try:
        payload = jwt.decode(
            token=token, key=SECRET_KEY, algorithms=[ALGORITHM]
        )
        user_id = payload.get("user_id")

        if not user_id:
            raise credentials_exception

        token_payload = TokenPayload(user_id=user_id)
    except JWTError:
        raise credentials_exception

    return token_payload


def get_current_user(
    token: str = Depends(OAUTH2_SCHEMA), db: Session = Depends(get_db)
) -> TokenPayload:
    """
    The function returns a `user` that has the correct `payload` data.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    access_token = verify_access_token(
        token=token, credentials_exception=credentials_exception
    )
    user = db.query(User).filter(User.user_id == access_token.user_id).first()

    return user
