from fastapi import status
from fastapi.testclient import TestClient


def test_root(client: TestClient) -> None:
    response = client.get("/")

    assert response.json().get("message") == "Hi, there!"
    assert response.status_code == status.HTTP_200_OK
