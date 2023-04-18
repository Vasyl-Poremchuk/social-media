from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database import get_db
from src.models import Like, Post
from src.oauth2 import get_current_user
from src.schemas import LikeBase, LikeResponse

router = APIRouter(prefix="/likes", tags=["Like Endpoint"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def like_post(
    like: LikeBase,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    """
    The function creates or deletes an existing `like`.
    """
    post = db.query(Post).filter(Post.post_id == like.post_id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with post_id: {like.post_id} does not exist.",
        )

    if post.user_id == current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot like your own post.",
        )

    like_query = db.query(Like).filter(
        Like.post_id == like.post_id, Like.user_id == current_user.user_id
    )
    found_like = like_query.first()

    if like.liked:
        if found_like:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User with user_id: {current_user.user_id} "
                f"has already liked on post with post_id: {like.post_id}.",
            )
        new_like = Like(user_id=current_user.user_id, post_id=like.post_id)
        db.add(new_like)
        db.commit()

        return {"detail": "Successfully added like."}
    else:
        if not found_like:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Like does not exist.",
            )
        like_query.delete(synchronize_session=False)
        db.commit()

        return {"detail": "Successfully deleted like."}
