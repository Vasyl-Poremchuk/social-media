from typing import Type

from fastapi import status
from fastapi.testclient import TestClient
from pytest import mark

from src.models import Post
from src.schemas import PostResponse, PostLikeCommentResponse


def test_get_posts(
    authorized_client: TestClient, test_posts: list[Type[Post]]
) -> None:
    print(test_posts)
    response = authorized_client.get("/posts/")
    posts = [PostLikeCommentResponse(**post) for post in response.json()]

    assert len(posts) == len(test_posts)
    assert response.status_code == status.HTTP_200_OK


def test_unauthorized_user_get_posts(
    client: TestClient, test_posts: list[Type[Post]]
) -> None:
    response = client.get("/posts/")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_unauthorized_user_get_post(
    client: TestClient, test_posts: list[Type[Post]]
) -> None:
    response = client.get(f"/posts/{test_posts[0].post_id}")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_post_not_exist(
    authorized_client: TestClient, test_posts: list[Type[Post]]
) -> None:
    response = authorized_client.get("/posts/7")

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_post(
    authorized_client: TestClient, test_posts: list[Type[Post]]
) -> None:
    response = authorized_client.get(f"/posts/{test_posts[0].post_id}")
    post = PostLikeCommentResponse(**response.json())

    assert post.Post.post_id == test_posts[0].post_id
    assert post.Post.title == test_posts[0].title
    assert post.Post.content == test_posts[0].content
    assert post.Post.category == test_posts[0].category


@mark.parametrize(
    "title, content, category",
    [
        (
            "The Pros and Cons of Remote Work",
            "Remote work has become increasingly popular in recent years, "
            "but is it right for everyone? In this post, we'll explore "
            "the pros and cons of remote work and help you decide if it's "
            "a good fit for you.",
            "BUSINESS",
        ),
        (
            "10 Educational Resources for Lifelong Learners",
            "Expand your knowledge with these educational resources, "
            "including online courses and educational apps, to support "
            "your lifelong learning and personal growth in various fields.",
            "EDUCATION",
        ),
        (
            "10 Latest Technology Trends to Watch",
            "Stay up-to-date with the latest technology trends, "
            "including advancements in artificial intelligence, virtual reality, "
            "blockchain, and more, that are shaping the future of various industries.",
            "TECHNOLOGY",
        ),
    ],
)
def test_create_post(
    authorized_client: TestClient,
    test_user: dict,
    test_posts: list[Type[Post]],
    title: str,
    content: str,
    category: str,
) -> None:
    response = authorized_client.post(
        "/posts/",
        json={"title": title, "content": content, "category": category},
    )
    post = PostResponse(**response.json())

    assert post.title == title
    assert post.content == content
    assert post.category == category
    assert post.author.user_id == test_user["user_id"]
    assert response.status_code == status.HTTP_201_CREATED


@mark.parametrize(
    "title, content, category",
    [
        (
            "10 Inspiring Sports Stories of Triumph and Resilience",
            "Be inspired by these heartwarming sports stories that highlight "
            "the triumph of the human spirit, featuring athletes who have overcome "
            "challenges and achieved remarkable success in their respective sports.",
            "SPORTS",
        ),
        (
            "10 Hot Topics in Politics Today",
            "Stay informed about the latest hot topics in politics, including current events, "
            "policy debates, and global issues that are shaping the political landscape.",
            "POLITICS",
        ),
    ],
)
def test_unauthorized_user_create_post(
    client: TestClient,
    test_user: dict,
    test_posts: list[Type[Post]],
    title: str,
    content: str,
    category: str,
):
    response = client.post(
        "/posts/",
        json={"title": title, "content": content, "category": category},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_post(
    authorized_client: TestClient,
    test_user: dict,
    test_posts: list[Type[Post]],
) -> None:
    data = {
        "title": "10 Personal Finance Tips for a Secure Future",
        "content": "Learn essential personal finance tips for managing your money, "
        "saving for the future, and building financial security for yourself "
        "and your family.",
        "category": "PERSONAL",
    }
    response = authorized_client.put(
        f"/posts/{test_posts[0].post_id}", json=data
    )
    updated_post = PostResponse(**response.json())

    assert updated_post.title == data["title"]
    assert updated_post.content == data["content"]
    assert updated_post.category == data["category"]
    assert response.status_code == status.HTTP_200_OK


def test_update_other_user_post(
    authorized_client: TestClient,
    test_user: dict,
    test_user_second: dict,
    test_posts: list[Type[Post]],
) -> None:
    data = {
        "title": "10 Personal Finance Tips for a Secure Future",
        "content": "Learn essential personal finance tips for managing your money, "
        "saving for the future, and building financial security for yourself "
        "and your family.",
        "category": "PERSONAL",
        "post_id": test_posts[2].post_id,
    }
    response = authorized_client.put(
        f"/posts/{test_posts[2].post_id}", json=data
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_unauthorized_user_update_post(
    client: TestClient, test_user: dict, test_posts: list[Type[Post]]
) -> None:
    response = client.put(f"/posts/{test_posts[0].post_id}")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_post_non_exist(
    authorized_client: TestClient,
    test_user: dict,
    test_posts: list[Type[Post]],
) -> None:
    data = {
        "title": "10 Personal Finance Tips for a Secure Future",
        "content": "Learn essential personal finance tips for managing your money, "
        "saving for the future, and building financial security for yourself "
        "and your family.",
        "category": "PERSONAL",
        "post_id": test_posts[2].post_id,
    }
    response = authorized_client.put("/posts/7", json=data)

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_unauthorized_user_delete_post(
    client: TestClient, test_user: dict, test_posts: list[Type[Post]]
) -> None:
    response = client.delete(f"/posts/{test_posts[0].post_id}")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_delete_post(
    authorized_client: TestClient,
    test_user: dict,
    test_posts: list[Type[Post]],
) -> None:
    response = authorized_client.delete(f"/posts/{test_posts[0].post_id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_post_non_exist(
    authorized_client: TestClient,
    test_user: dict,
    test_posts: list[Type[Post]],
) -> None:
    response = authorized_client.delete("/posts/7")

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_other_user_post(
    authorized_client: TestClient,
    test_user: dict,
    test_posts: list[Type[Post]],
):
    response = authorized_client.delete(f"/posts/{test_posts[2].post_id}")

    assert response.status_code == status.HTTP_403_FORBIDDEN
