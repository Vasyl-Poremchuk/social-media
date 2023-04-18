from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    """
    The function converts the user's `password`
    to a `hashed` version of `password`.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    The function checks whether the entered `password` matches
    an existing `password` in the database.
    """
    return pwd_context.verify(plain_password, hashed_password)
