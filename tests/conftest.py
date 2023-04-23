from typing import Type

from fastapi import status
from fastapi.testclient import TestClient
from pytest import fixture
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from src.config import settings
from src.database import get_db
from src.main import app
from src.models import Base, Comment, Post
from src.oauth2 import create_access_token


SQLALCHEMY_DATABASE_URL = (
    f"postgresql://"
    f"{settings.POSTGRES_USER}:"
    f"{settings.POSTGRES_PASSWORD}@"
    f"{settings.POSTGRES_HOST}:"
    f"{settings.POSTGRES_PORT}/"
    f"{settings.POSTGRES_DB}_test"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)


@fixture
def session() -> Session:
    """
    The function to create and close the test session database,
    and to delete all and create new values in the test database.
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@fixture
def client(session: Session) -> TestClient:
    """
    Test client initialization function.
    """

    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app=app)


@fixture
def test_user(client: TestClient) -> dict:
    """
    The function creates a first test user.
    """
    user_data = {
        "username": "jessica",
        "email": "jessica@gmail.com",
        "password": "!Jessica123",
    }
    response = client.post("/users/", json=user_data)

    assert response.status_code == status.HTTP_201_CREATED

    new_user = response.json()
    new_user["password"] = user_data["password"]

    return new_user


@fixture
def test_user_second(client: TestClient) -> dict:
    """
    The function creates a second test user.
    """
    user_data_second = {
        "username": "jones",
        "email": "jones@gmail.com",
        "password": "!Jones123",
    }
    response = client.post("/users/", json=user_data_second)

    assert response.status_code == status.HTTP_201_CREATED

    new_user = response.json()
    new_user["password"] = user_data_second["password"]

    return new_user


@fixture
def token(test_user: dict) -> str:
    """
    The function creates an access token for the first test user.
    """
    return create_access_token({"user_id": test_user["user_id"]})


@fixture
def authorized_client(client: TestClient, token: str) -> TestClient:
    """
    Function that makes authorization for the first test user.
    """
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}

    return client


@fixture
def test_posts(
    test_user: dict, test_user_second: dict, session: Session
) -> list[Type[Post]]:
    """
    The function creates posts in the test database.
    """
    posts_data = [
        {
            "title": "The Impact of Climate Change on Agriculture",
            "content": "Climate change is affecting agriculture in many ways, "
            "from unpredictable weather patterns to the spread of "
            "pests and diseases. Farmers are struggling to adapt to "
            "these changes and maintain their livelihoods.",
            "category": "ENVIRONMENT",
            "user_id": test_user["user_id"],
        },
        {
            "title": "How to Improve Your Public Speaking Skills",
            "content": "Public speaking is an essential skill for success "
            "in many careers. In this post, we'll explore some "
            "tips and tricks for improving your public speaking skills, "
            "from preparation to delivery.",
            "category": "EDUCATION",
            "user_id": test_user["user_id"],
        },
        {
            "title": "10 Delicious Recipes for Vegan Burgers",
            "content": "Whether you're a vegan or just looking to add more "
            "plant-based meals to your diet, these vegan burger "
            "recipes are sure to satisfy. From classic veggie burgers "
            "to creative new twists, there's something for everyone.",
            "category": "FOOD",
            "user_id": test_user_second["user_id"],
        },
    ]
    posts = [Post(**post) for post in posts_data]

    session.add_all(posts)
    session.commit()

    return session.query(Post).all()


@fixture
def test_comments(
    test_user: dict,
    test_user_second: dict,
    test_posts: list[Type[Post]],
    session: Session,
) -> list[Type[Comment]]:
    """
    The function creates comments in the test database.
    """
    comments_data = [
        {
            "content": "Impressive content, it really made me think and reflect.",
            "post_id": test_posts[0].post_id,
            "user_id": test_user_second["user_id"],
        },
        {
            "content": "Well said! The content is on point and relevant.",
            "post_id": test_posts[1].post_id,
            "user_id": test_user_second["user_id"],
        },
        {
            "content": "Kudos! The content is top-notch and worth sharing.",
            "post_id": test_posts[2].post_id,
            "user_id": test_user["user_id"],
        },
    ]
    comments = [Comment(**comment) for comment in comments_data]

    session.add_all(comments)
    session.commit()

    return session.query(Comment).all()
