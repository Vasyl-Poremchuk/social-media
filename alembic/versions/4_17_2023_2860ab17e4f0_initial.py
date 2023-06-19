"""
initial

Revision ID: 2860ab17e4f0
Revises: 
Create Date: 2023-04-17 17:29:48.545808
"""
from alembic import op
import sqlalchemy as sa


revision = "2860ab17e4f0"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    The function upgrades all changes from a specific revision.
    """
    op.create_table(
        "user",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column(
            "is_active", sa.Boolean(), server_default="True", nullable=False
        ),
        sa.Column(
            "is_superuser",
            sa.Boolean(),
            server_default="False",
            nullable=False,
        ),
        sa.Column(
            "is_verified", sa.Boolean(), server_default="False", nullable=False
        ),
        sa.Column("first_name", sa.String(), nullable=True),
        sa.Column("last_name", sa.String(), nullable=True),
        sa.Column("phone_number", sa.String(), nullable=True),
        sa.Column("country", sa.String(), nullable=True),
        sa.Column("region", sa.String(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("user_id"),
        sa.UniqueConstraint("username"),
    )
    op.create_index(op.f("ix_user_email"), "user", ["email"], unique=True)
    op.create_index(op.f("ix_user_user_id"), "user", ["user_id"], unique=False)
    op.create_table(
        "post",
        sa.Column("post_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("content", sa.String(), nullable=False),
        sa.Column(
            "category",
            sa.Enum(
                "BUSINESS",
                "EDUCATION",
                "ENTERTAINMENT",
                "ENVIRONMENT",
                "FOOD",
                "LIFESTYLE",
                "PERSONAL",
                "POLITICS",
                "SPORTS",
                "TECHNOLOGY",
                name="category",
            ),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"], ["user.user_id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("post_id"),
    )
    op.create_index(op.f("ix_post_post_id"), "post", ["post_id"], unique=False)
    op.create_table(
        "comment",
        sa.Column("comment_id", sa.Integer(), nullable=False),
        sa.Column("content", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("post_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["post_id"], ["post.post_id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["user.user_id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("comment_id"),
    )
    op.create_index(
        op.f("ix_comment_comment_id"), "comment", ["comment_id"], unique=False
    )
    op.create_table(
        "like",
        sa.Column("like_id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("post_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["post_id"], ["post.post_id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["user.user_id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("like_id"),
        sa.UniqueConstraint("user_id", "post_id", name="uq_user_post"),
    )
    op.create_index(op.f("ix_like_like_id"), "like", ["like_id"], unique=False)


def downgrade() -> None:
    """
    The function downgrades all changes from a specific revision.
    """
    op.drop_index(op.f("ix_like_like_id"), table_name="like")
    op.drop_table("like")
    op.drop_index(op.f("ix_comment_comment_id"), table_name="comment")
    op.drop_table("comment")
    op.drop_index(op.f("ix_post_post_id"), table_name="post")
    op.drop_table("post")
    op.drop_index(op.f("ix_user_user_id"), table_name="user")
    op.drop_index(op.f("ix_user_email"), table_name="user")
    op.drop_table("user")
