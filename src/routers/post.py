from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from src.database import get_db
from src.models import Post, Like, Comment
from src.oauth2 import get_current_user
from src.schemas import (
    PostResponse,
    PostCreate,
    PostUpdate,
    PostLikeCommentResponse,
)

router = APIRouter(prefix="/posts", tags=["Post Endpoints"])


@router.get("/", response_model=list[PostLikeCommentResponse])
def get_posts(
    db: Session = Depends(get_db),
    offset: int = 0,
    limit: int = 10,
    current_user: int = Depends(get_current_user),
) -> list[PostResponse]:
    """
    The function returns a list of `posts` from the database,
    with optional pagination parameters to limit the number of `posts` returned.
    """
    posts = (
        db.query(
            Post,
            func.count(Like.post_id).label("likes"),
            func.count(Comment.post_id).label("comments"),
        )
        .outerjoin(Like, Like.post_id == Post.post_id)
        .outerjoin(Comment, Comment.post_id == Post.post_id)
        .group_by(Post.post_id)
        .limit(limit)
        .offset(offset)
        .all()
    )

    return posts


@router.get("/{post_id}", response_model=PostLikeCommentResponse)
def get_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
) -> PostResponse:
    """
    The function returns a single `post` from the database.
    """
    # post = db.query(Post).filter(Post.post_id == post_id).first()
    post = (
        db.query(
            Post,
            func.count(Like.post_id).label("likes"),
            func.count(Comment.post_id).label("comments"),
        )
        .outerjoin(Like, Like.post_id == Post.post_id)
        .outerjoin(Comment, Comment.post_id == Post.post_id)
        .group_by(Post.post_id)
        .filter(Post.post_id == post_id)
        .first()
    )

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with post_id: {post_id} was not found.",
        )

    return post


@router.post(
    "/",
    response_model=PostResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_post(
    post: PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
) -> PostResponse:
    """
    The function creates a new `post` in the database.
    """
    new_post = Post(user_id=current_user.user_id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.put("/{post_id}", response_model=PostResponse)
def update_post(
    post_id: int,
    post: PostUpdate,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
) -> PostResponse:
    """
    The function updates an existing `post` in the database.
    """
    post_query = db.query(Post).filter(Post.post_id == post_id)
    updated_post = post_query.first()

    if not updated_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with post_id: {post_id} does not exist.",
        )

    if updated_post.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform request action.",
        )

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
) -> None:
    """
    The function deletes an existing `post` in the database.
    """
    post_query = db.query(Post).filter(Post.post_id == post_id)
    post = post_query.first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with post_id: {post_id} does not exist.",
        )

    if post.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform request action.",
        )

    post_query.delete(synchronize_session=False)
    db.commit()
