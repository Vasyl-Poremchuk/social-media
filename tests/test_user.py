from fastapi import status
from fastapi.testclient import TestClient
from jose import jwt
from pytest import mark

from src.oauth2 import SECRET_KEY, ALGORITHM
from src.schemas import UserResponse, Token


def test_create_user(client: TestClient) -> None:
    response = client.post(
        "/users/",
        json={
            "username": "jessica",
            "email": "jessica@gmail.com",
            "password": "!Jessica123",
        },
    )
    new_user = UserResponse(**response.json())

    assert new_user.email == "jessica@gmail.com"
    assert response.status_code == status.HTTP_201_CREATED


def test_login_user(client: TestClient, test_user: dict) -> None:
    response = client.post(
        "/login/",
        data={
            "username": test_user["email"],
            "password": test_user["password"],
        },
    )
    login_response = Token(**response.json())
    payload = jwt.decode(
        token=login_response.access_token,
        key=SECRET_KEY,
        algorithms=[ALGORITHM],
    )
    user_id = payload.get("user_id")

    assert user_id == test_user["user_id"]
    assert response.status_code == status.HTTP_200_OK
    assert login_response.token_type == "bearer"


@mark.parametrize(
    "email, password, status_code",
    [
        ("essica@gmail.com", "!Jessica123", status.HTTP_403_FORBIDDEN),
        ("jessica@gmail.com", "!Jesica123", status.HTTP_403_FORBIDDEN),
        ("essica@gmail.com", "!Jesica123", status.HTTP_403_FORBIDDEN),
        (None, "!Jessica123", status.HTTP_422_UNPROCESSABLE_ENTITY),
        ("jessica@gmail.com", None, status.HTTP_422_UNPROCESSABLE_ENTITY),
    ],
)
def test_incorrect_login(
    test_user: dict,
    client: TestClient,
    email: str | None,
    password: str | None,
    status_code: str,
):
    response = client.post(
        "/login/",
        data={"username": email, "password": password},
    )

    assert response.status_code == status_code
