class UsernameFormatError(Exception):
    """
    Custom error that is raised when `username` does not have the right format.
    """

    def __init__(self, username: str, message: str) -> None:
        self.username = username
        self.message = message
        super().__init__(message)


class PasswordFormatError(Exception):
    """
    Custom error that is raised when `password` does not have the right format.
    """

    def __init__(self, password: str, message: str) -> None:
        self.password = password
        self.message = message
        super().__init__(message)


class FirstNameFormatError(Exception):
    """
    Custom error that is raised when `first_name` does not have the right format.
    """

    def __init__(self, first_name: str, message: str) -> None:
        self.first_name = first_name
        self.message = message
        super().__init__(message)


class LastNameFormatError(Exception):
    """
    Custom error that is raised when `last_name` does not have the right format.
    """

    def __init__(self, last_name: str, message: str) -> None:
        self.last_name = last_name
        self.message = message
        super().__init__(message)


class PhoneNumberFormatError(Exception):
    """
    Custom error that is raised when `phone_number` does not have the right format.
    """

    def __init__(self, phone_number: str, message: str) -> None:
        self.phone_number = phone_number
        self.message = message
        super().__init__(message)


class CountryFormatError(Exception):
    """
    Custom error that is raised when `country` does not have the right format.
    """

    def __init__(self, country: str, message: str) -> None:
        self.country = country
        self.message = message
        super().__init__(message)


class RegionFormatError(Exception):
    """
    Custom error that is raised when `region` does not have the right format.
    """

    def __init__(self, region: str, message: str) -> None:
        self.region = region
        self.message = message
        super().__init__(message)


class TitleFormatError(Exception):
    """
    Custom error that is raised when `title` does not have the right format.
    """

    def __init__(self, title: str, message: str) -> None:
        self.title = title
        self.message = message
        super().__init__(message)


class ContentFormatError(Exception):
    """
    Custom error that is raised when `content` does not have the right format.
    """

    def __init__(self, content: str, message: str) -> None:
        self.content = content
        self.message = message
        super().__init__(message)
