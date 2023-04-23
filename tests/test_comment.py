from typing import Type

from fastapi import status
from fastapi.testclient import TestClient
from pytest import mark

from src.models import Comment
from src.schemas import CommentResponse


def test_get_comments(
    authorized_client: TestClient, test_comments: list[Type[Comment]]
) -> None:
    response = authorized_client.get("/comments/")
    comments = [CommentResponse(**comment) for comment in response.json()]

    assert len(comments) == len(test_comments)
    assert response.status_code == status.HTTP_200_OK


def test_unauthorized_user_get_comments(
    client: TestClient, test_comments: list[Type[Comment]]
) -> None:
    response = client.get("/comments/")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_unauthorized_user_get_comment(
    client: TestClient, test_comments: list[Type[Comment]]
) -> None:
    response = client.get(f"/comments/{test_comments[0].comment_id}")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_comment_non_exist(
    authorized_client: TestClient, test_comments: list[Type[Comment]]
) -> None:
    response = authorized_client.get("/comments/7")

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_comment(
    authorized_client: TestClient, test_comments: list[Type[Comment]]
) -> None:
    response = authorized_client.get(
        f"/comments/{test_comments[0].comment_id}"
    )
    comment = CommentResponse(**response.json())

    assert comment.comment_id == test_comments[0].comment_id
    assert comment.content == test_comments[0].content
    assert comment.post_id == test_comments[0].post_id
    assert comment.author.user_id == test_comments[0].user_id


@mark.parametrize(
    "content, post_id, user_id",
    [
        (
            "Excellent post! The content is engaging and informative.",
            1,
            2,
        ),
        (
            "Love the content! It's insightful and beautifully expressed.",
            2,
            2,
        ),
        (
            "Brilliant content, it captured my attention and kept me hooked.",
            3,
            1,
        ),
    ],
)
def test_create_comment(
    authorized_client: TestClient,
    test_user: dict,
    test_comments: list[Type[Comment]],
    content: str,
    post_id: int,
    user_id: int,
) -> None:
    response = authorized_client.post(
        "/comments/",
        json={"content": content, "post_id": post_id, "user_id": user_id},
    )
    comment = CommentResponse(**response.json())

    assert comment.content == content
    assert comment.post_id == post_id
    assert comment.author.user_id == test_user["user_id"]
    assert response.status_code == status.HTTP_201_CREATED


@mark.parametrize(
    "content, post_id, user_id",
    [
        (
            "Spot-on! The content is concise and impactful.",
            1,
            2,
        ),
        (
            "Powerful words! The content speaks volumes.",
            2,
            2,
        ),
    ],
)
def test_unauthorized_user_create_comment(
    client: TestClient,
    test_user: dict,
    test_comments: list[Type[Comment]],
    content: str,
    post_id: int,
    user_id: int,
) -> None:
    response = client.post(
        "/comments/",
        json={"content": content, "post_id": post_id, "user_id": user_id},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_comment(
    authorized_client: TestClient,
    test_user_second: dict,
    test_comments: list[Type[Comment]],
) -> None:
    data = {
        "content": "Bravo! The content is a valuable contribution to the topic.",
        "post_id": 3,
        "user_id": 1,
    }
    response = authorized_client.put(
        f"/comments/{test_comments[2].comment_id}", json=data
    )
    updated_comment = CommentResponse(**response.json())

    assert updated_comment.content == data["content"]
    assert updated_comment.post_id == data["post_id"]
    assert updated_comment.author.user_id == data["user_id"]
    assert response.status_code == status.HTTP_200_OK


def test_update_other_user_comment(
    authorized_client: TestClient,
    test_user: dict,
    test_user_second: dict,
    test_comments: list[Type[Comment]],
) -> None:
    data = {
        "content": "Bravo! The content is a valuable contribution to the topic.",
        "post_id": 1,
        "user_id": 2,
        "comment_id": test_comments[1].comment_id,
    }
    response = authorized_client.put(
        f"/comments/{test_comments[1].comment_id}", json=data
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_unauthorized_user_update_comment(
    client: TestClient, test_user: dict, test_comments: list[Type[Comment]]
) -> None:
    response = client.put(f"/comments/{test_comments[0].comment_id}")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_comment_non_exist(
    authorized_client: TestClient,
    test_user: dict,
    test_comments: list[Type[Comment]],
) -> None:
    data = {
        "content": "Bravo! The content is a valuable contribution to the topic.",
        "post_id": 1,
        "user_id": 2,
        "comment_id": test_comments[0].comment_id,
    }
    response = authorized_client.put("/comments/7", json=data)

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_unauthorized_user_delete_comment(
    client: TestClient, test_user: dict, test_comments: list[Type[Comment]]
) -> None:
    response = client.delete(f"/comments/{test_comments[1].comment_id}")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_delete_comment(
    authorized_client: TestClient,
    test_user: dict,
    test_comments: list[Type[Comment]],
) -> None:
    response = authorized_client.delete(
        f"/comments/{test_comments[2].comment_id}"
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_comment_non_exist(
    authorized_client: TestClient,
    test_user: dict,
    test_comments: list[Type[Comment]],
) -> None:
    response = authorized_client.delete("/comments/7")

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_other_user_comment(
    authorized_client: TestClient,
    test_user: dict,
    test_comments: list[Type[Comment]],
) -> None:
    response = authorized_client.delete(
        f"/comments/{test_comments[0].post_id}"
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
