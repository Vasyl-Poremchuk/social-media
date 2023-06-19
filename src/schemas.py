import re
from datetime import datetime
from string import punctuation

from pydantic import BaseModel, EmailStr, validator

from src.exceptions import (
    ContentFormatException,
    CountryFormatException,
    FirstNameFormatException,
    LastNameFormatException,
    PasswordFormatException,
    PhoneNumberFormatException,
    TitleFormatException,
    UsernameFormatException,
)
from src.models import Category


PHONE_NUMBER_REGEX = re.compile(
    r"^(?:\+38|0)?\(?0?\d{2}\)?\s?\d{3}-?\d{2}-?\d{2}$"
)
PUNCTUATION_WITHOUT_UNDERSCORE = punctuation.replace("_", "")


def validate_content(content: str) -> str:
    """
    The function checks if the `content` passes all validations.
    """
    if all(
        character.isdigit() or character.isspace() or character in punctuation
        for character in content
    ):
        raise ContentFormatException(
            detail="The `content` must contain letters.",
        )
    return content


class UserBase(BaseModel):
    username: str
    email: EmailStr
    password: str
    first_name: str | None = None
    last_name: str | None = None
    phone_number: str | None = None
    country: str | None = None
    region: str | None = None

    @validator("username")
    def validate_username(cls, value: str) -> str:
        """
        The method checks if the `username` passes all validations.
        """
        if not (5 <= len(value) <= 15):
            raise UsernameFormatException(
                detail="The length of the `username` must be between 5 and 15 characters.",
            )

        if any(character.isupper() for character in value):
            raise UsernameFormatException(
                detail="The `username` must not contain uppercase characters.",
            )

        if any(character.isspace() for character in value):
            raise UsernameFormatException(
                detail="The `username` must not contain whitespaces.",
            )

        if any(
            character in PUNCTUATION_WITHOUT_UNDERSCORE for character in value
        ):
            raise UsernameFormatException(
                detail="The `username` must not contain any punctuation marks other than underscores.",
            )

        return value

    @validator("password")
    def validate_password(cls, value: str) -> str:
        """
        The function checks if the `password` passes all validations.
        """
        if len(value) < 8:
            raise PasswordFormatException(
                detail="The `password` must be at least 8 characters long.",
            )

        if not any(character.isupper() for character in value):
            raise PasswordFormatException(
                detail="The `password` must contain at least one uppercase letter.",
            )

        if not any(character.islower() for character in value):
            raise PasswordFormatException(
                detail="The `password` must contain at least one lowercase letter.",
            )

        if not any(character.isdigit() for character in value):
            raise PasswordFormatException(
                detail="The `password` must contain at least one digit.",
            )

        if not any(character in punctuation for character in value):
            raise PasswordFormatException(
                detail="The `password` must contain at least one punctuation mark "
                "such as !#$%&'\"()*+,-/:;<=>?@[\\]^_`{|}~.",
            )

        if any(character.isspace() for character in value):
            raise PasswordFormatException(
                detail="The `password` must not contain whitespaces.",
            )

        return value

    @validator("first_name")
    def validate_first_name(cls, value: str) -> str:
        """
        The method checks if the `first_name` passes all validations.
        """
        if value:
            if any(character.isspace() for character in value):
                raise FirstNameFormatException(
                    detail="The `first_name` must not contain whitespaces.",
                )

            if any(character.isdigit() for character in value):
                raise FirstNameFormatException(
                    detail="The `first_name` must not contain digits.",
                )

            if any(character in punctuation for character in value):
                raise FirstNameFormatException(
                    detail="The `first_name` must not contain punctuation marks.",
                )

            if not value.istitle():
                raise FirstNameFormatException(
                    detail="The `first_name` must start with a capital letter.",
                )

        return value

    @validator("last_name")
    def validate_last_name(cls, value: str) -> str:
        """
        The method checks if the `last_name` passes all validations.
        """
        if value:
            if any(character.isspace() for character in value):
                raise LastNameFormatException(
                    detail="The `last_name` must not contain whitespaces.",
                )

            if any(character.isdigit() for character in value):
                raise LastNameFormatException(
                    detail="The `last_name` must not contain digits.",
                )

            if any(character in punctuation for character in value):
                raise LastNameFormatException(
                    detail="The `last_name` must not contain punctuation marks.",
                )

            if not value.istitle():
                raise LastNameFormatException(
                    detail="The `last_name` must start with a capital letter.",
                )

        return value

    @validator("phone_number")
    def validate_phone_number(cls, value: str) -> str:
        """
        The method checks if the `phone_number` passes all validations.
        """
        if value:
            if not PHONE_NUMBER_REGEX.match(value):
                raise PhoneNumberFormatException(
                    detail="The `phone_number` is in the wrong format.",
                )

        return value

    @validator("country")
    def validate_country(cls, value: str) -> str:
        """
        The method checks if the `country` passes all validations.
        """
        if value:
            if any(character in punctuation for character in value):
                raise CountryFormatException(
                    detail="The `country` must not contain punctuation marks.",
                )

            if any(character.isdigit() for character in value):
                raise CountryFormatException(
                    detail="The `country` must not contain digits.",
                )

            if not value.istitle():
                raise CountryFormatException(
                    detail="The `country` must start with a capital letter.",
                )

        return value

    @validator("region")
    def validate_region(cls, value: str) -> str:
        """
        The method checks if the `region` passes all validations.
        """
        if value:
            if any(character in punctuation for character in value):
                raise CountryFormatException(
                    detail="The `region` must not contain punctuation marks.",
                )

            if any(character.isdigit() for character in value):
                raise CountryFormatException(
                    detail="The `region` must not contain digits.",
                )

            if not value.istitle():
                raise CountryFormatException(
                    detail="The `region` must start with a capital letter.",
                )

        return value


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    user_id: int
    is_active: bool
    is_superuser: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class UserSummaryResponse(BaseModel):
    user_id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    user_id: int | None = None


class CommentBase(BaseModel):
    content: str
    post_id: int

    _validate_content = validator("content", allow_reuse=True)(
        validate_content
    )


class CommentCreate(CommentBase):
    pass


class CommentUpdate(CommentBase):
    pass


class CommentResponse(CommentBase):
    comment_id: int
    created_at: datetime
    updated_at: datetime
    author: UserSummaryResponse

    class Config:
        orm_mode = True


class LikeBase(BaseModel):
    post_id: int
    liked: bool


class LikeResponse(LikeBase):
    like_id: int
    created_at: datetime
    user: UserSummaryResponse

    class Config:
        orm_mode = True


class PostBase(BaseModel):
    title: str
    content: str
    category: Category

    @validator("title")
    def validate_title(cls, value: str) -> str:
        """
        The method checks if the `title` passes all validations.
        """
        if all(
            character.isdigit()
            or character.isspace()
            or character in punctuation
            for character in value
        ):
            raise TitleFormatException(
                detail="The `title` must contain letters.",
            )

        return value

    _validate_content = validator("content", allow_reuse=True)(
        validate_content
    )


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass


class PostResponse(PostBase):
    post_id: int
    created_at: datetime
    updated_at: datetime
    author: UserSummaryResponse

    class Config:
        orm_mode = True


class PostLikeCommentResponse(BaseModel):
    Post: PostResponse
    likes: int
    comments: int

    class Config:
        orm_mode = True
