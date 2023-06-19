from fastapi.exceptions import HTTPException
from starlette import status


class UsernameFormatException(HTTPException):
    """
    A custom exception is raised when the `username` has an incorrect format.
    """

    def __init__(self, detail: str) -> None:
        self.detail = detail
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail
        )


class PasswordFormatException(HTTPException):
    """
    A custom exception is raised when the `password` has an incorrect format.
    """

    def __init__(self, detail: str) -> None:
        self.detail = detail
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail
        )


class FirstNameFormatException(HTTPException):
    """
    A custom exception is raised when the `first_name` has an incorrect format.
    """

    def __init__(self, detail: str) -> None:
        self.detail = detail
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail
        )


class LastNameFormatException(HTTPException):
    """
    A custom exception is raised when the `last_name` has an incorrect format.
    """

    def __init__(self, detail: str) -> None:
        self.detail = detail
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail
        )


class PhoneNumberFormatException(HTTPException):
    """
    A custom exception is raised when the `phone_number` has an incorrect format.
    """

    def __init__(self, detail: str) -> None:
        self.detail = detail
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail
        )


class CountryFormatException(HTTPException):
    """
    A custom exception is raised when the `country` has an incorrect.
    """

    def __init__(self, detail: str) -> None:
        self.detail = detail
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail
        )


class RegionFormatException(HTTPException):
    """
    A custom exception is raised when the `region` has an incorrect format.
    """

    def __init__(self, detail: str) -> None:
        self.detail = detail
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail
        )


class TitleFormatException(HTTPException):
    """
    A custom exception is raised when the `title` has an incorrect format.
    """

    def __init__(self, detail: str) -> None:
        self.detail = detail
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail
        )


class ContentFormatException(HTTPException):
    """
    A custom exception is raised when the `content` has an incorrect format.
    """

    def __init__(self, detail: str) -> None:
        self.detail = detail
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail
        )
