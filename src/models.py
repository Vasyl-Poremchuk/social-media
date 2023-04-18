from enum import Enum

import sqlalchemy.types
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    func,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class Category(str, Enum):
    BUSINESS = "BUSINESS"
    EDUCATION = "EDUCATION"
    ENTERTAINMENT = "ENTERTAINMENT"
    ENVIRONMENT = "ENVIRONMENT"
    FOOD = "FOOD"
    LIFESTYLE = "LIFESTYLE"
    PERSONAL = "PERSONAL"
    POLITICS = "POLITICS"
    SPORTS = "SPORTS"
    TECHNOLOGY = "TECHNOLOGY"


class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True, index=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, server_default="True", nullable=False)
    is_superuser = Column(Boolean, server_default="False", nullable=False)
    is_verified = Column(Boolean, server_default="False", nullable=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    country = Column(String, nullable=True)
    region = Column(String, nullable=True)
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    posts = relationship("Post", back_populates="author")
    comments = relationship("Comment", back_populates="author")
    likes = relationship("Like", back_populates="user")

    def __repr__(self) -> str:
        return (
            f"User(user_id={self.user_id}, "
            f"username={self.username}, "
            f"first_name={self.first_name}, "
            f"last_name={self.last_name})"
        )


class Post(Base):
    __tablename__ = "post"

    post_id = Column(Integer, primary_key=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    category = Column(sqlalchemy.types.Enum(Category), nullable=False)
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    user_id = Column(
        Integer, ForeignKey("user.user_id", ondelete="CASCADE"), nullable=False
    )
    author = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")
    likes = relationship("Like", back_populates="post")

    def __repr__(self) -> str:
        return f"Post(post_id={self.post_id}, created_at={self.created_at})"


class Comment(Base):
    __tablename__ = "comment"

    comment_id = Column(Integer, primary_key=True, index=True, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    post_id = Column(
        Integer, ForeignKey("post.post_id", ondelete="CASCADE"), nullable=False
    )
    user_id = Column(
        Integer, ForeignKey("user.user_id", ondelete="CASCADE"), nullable=False
    )
    author = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")

    def __repr__(self) -> str:
        return (
            f"Comment(comment_id={self.comment_id}, "
            f"created_at={self.created_at})"
        )


class Like(Base):
    __tablename__ = "like"

    like_id = Column(Integer, primary_key=True, index=True, nullable=False)
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    user_id = Column(
        Integer,
        ForeignKey("user.user_id", ondelete="CASCADE"),
        nullable=False,
    )
    post_id = Column(
        Integer,
        ForeignKey("post.post_id", ondelete="CASCADE"),
        nullable=False,
    )
    user = relationship("User", back_populates="likes")
    post = relationship("Post", back_populates="likes")

    __table_args__ = (
        UniqueConstraint("user_id", "post_id", name="uq_user_post"),
    )

    def __repr__(self) -> str:
        return f"Like(like_id={self.like_id}, created_at={self.created_at})"
