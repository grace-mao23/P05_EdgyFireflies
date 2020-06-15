import os
import pytest

from flask import Flask, Response
from flask.testing import FlaskClient

from app import create_app, db
from app.models import User


@pytest.fixture
def app() -> Flask:
    """
    Create and configure a new test app instance.

    :param: None
    
    :return: Flask
    """
    assert 2 + 2 == 4

    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })

    with app.app_context():
        db.drop_all()
        db.create_all()

        user = User(username="test", display_name="Tester", password="test")

        db.session.add(user)

        db.session.commit()

    yield app


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    """
    Create a test client for the test app instance.

    :param Flask app: A test app instance.

    :return: FlaskClient
    """
    return app.test_client()


class AuthActions:
    """
    Define the authentication class for testing.

    :method register:
    :method login:
    :method logout:
    """
    def __init__(self, client: FlaskClient):
        self._client = client

    def register(self,
                 username: str = "a",
                 display_name: str = "Tester",
                 password: str = "a") -> Response:
        return self._client.post("/auth/register",
                                 data={
                                     "username": username,
                                     "display_name": display_name,
                                     "password": password
                                 })

    def login(self,
              username: str = "test",
              password: str = "test") -> Response:
        return self._client.post("/auth/login",
                                 data={
                                     "username": username,
                                     "password": password
                                 })

    def logout(self) -> Response:
        return self._client.get("/auth/logout")


@pytest.fixture
def auth(client: FlaskClient) -> AuthActions:
    """
    Create an AuthActions class.

    :param FlaskClient client: A test client for the given app instance.
    
    :return: AuthActions
    """
    return AuthActions(client)
