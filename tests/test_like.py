from typing import Type

from fastapi import status
from fastapi.testclient import TestClient
from pytest import fixture
from sqlalchemy.orm import Session

from src.models import Post, Like


@fixture
def test_like(
    test_posts: list[Type[Post]], session: Session, test_user: dict
) -> None:
    new_like = Like(
        post_id=test_posts[2].post_id, user_id=test_user["user_id"]
    )

    session.add(new_like)
    session.commit()


def test_like_on_post(
    authorized_client: TestClient, test_posts: list[Type[Post]]
) -> None:
    response = authorized_client.post(
        "/likes/", json={"post_id": test_posts[2].post_id, "liked": True}
    )

    assert response.status_code == status.HTTP_201_CREATED


def test_like_twice_post(
    authorized_client: TestClient,
    test_posts: list[Type[Post]],
    test_like: None,
) -> None:
    response = authorized_client.post(
        "/likes/", json={"post_id": test_posts[2].post_id, "liked": True}
    )

    assert response.status_code == status.HTTP_409_CONFLICT


def test_delete_like(
    authorized_client: TestClient,
    test_posts: list[Type[Post]],
    test_like: None,
) -> None:
    response = authorized_client.post(
        "/likes/", json={"post_id": test_posts[2].post_id, "liked": False}
    )

    assert response.status_code == status.HTTP_201_CREATED


def test_delete_like_non_exist(
    authorized_client: TestClient, test_posts: list[Type[Post]]
) -> None:
    response = authorized_client.post(
        "/likes/", json={"post_id": test_posts[2].post_id, "liked": False}
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_like_post_non_exist(
    authorized_client: TestClient, test_posts: list[Type[Post]]
):
    response = authorized_client.post(
        "/likes/", json={"post_id": 7, "liked": False}
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_like_unauthorized_user(
    client: TestClient, test_posts: list[Type[Post]]
):
    response = client.post(
        "/likes/", json={"post_id": test_posts[2].post_id, "liked": True}
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
