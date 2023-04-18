from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database import get_db
from src.models import User
from src.schemas import UserResponse, UserCreate
from src.utils import get_hashed_password

router = APIRouter(prefix="/users", tags=["User Endpoints"])


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
) -> UserResponse:
    """
    The function returns a single `user` from the database.
    """
    user = db.query(User).filter(User.user_id == user_id).first()
    print(user)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with user_id: {user_id} does not exist.",
        )

    return user


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    user: UserCreate, db: Session = Depends(get_db)
) -> UserResponse:
    """
    The function creates a new `user` in the database.
    """
    hashed_password = get_hashed_password(user.password)
    user.password = hashed_password

    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
