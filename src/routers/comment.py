from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database import get_db
from src.models import Comment
from src.oauth2 import get_current_user
from src.schemas import CommentResponse, CommentCreate, CommentUpdate

router = APIRouter(prefix="/comments", tags=["Comment Endpoints"])


@router.get("/", response_model=list[CommentResponse])
def get_comments(
    db: Session = Depends(get_db),
    offset: int = 0,
    limit: int = 10,
    current_user: int = Depends(get_current_user),
) -> list[CommentResponse]:
    """
    The function returns a list of `comments` from the database,
    with optional pagination parameters to limit the number of `comments` returned.
    """
    comments = db.query(Comment).limit(limit=limit).offset(offset=offset).all()

    return comments


@router.get("/{comment_id}", response_model=CommentResponse)
def get_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
) -> CommentResponse:
    """
    The function returns a single `comment` from the database.
    """
    comment = (
        db.query(Comment).filter(Comment.comment_id == comment_id).first()
    )

    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Comment with comment_id: {comment_id} does not exist.",
        )

    return comment


@router.post(
    "/", response_model=CommentResponse, status_code=status.HTTP_201_CREATED
)
def create_comment(
    comment: CommentCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
) -> CommentResponse:
    """
    The function creates a new `comment` in the database.
    """
    new_comment = Comment(user_id=current_user.user_id, **comment.dict())
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return new_comment


@router.put("/{comment_id}", response_model=CommentResponse)
def update_comment(
    comment_id: int,
    comment: CommentUpdate,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
) -> CommentResponse:
    """
    The function updates an existing `comment` in the database.
    """
    comment_query = db.query(Comment).filter(Comment.comment_id == comment_id)
    updated_comment = comment_query.first()

    if not updated_comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Comment with comment_id: {comment_id} does not exist.",
        )

    if updated_comment.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform request action.",
        )

    comment_query.update(comment.dict(), synchronize_session=False)
    db.commit()

    return comment_query.first()


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
) -> None:
    """
    The function deletes an existing `comment` in the database.
    """
    comment_query = db.query(Comment).filter(Comment.comment_id == comment_id)
    comment = comment_query.first()

    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Comment with comment_id: {comment_id} does not exist.",
        )

    if comment.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform request action.",
        )

    comment_query.delete(synchronize_session=False)
    db.commit()
