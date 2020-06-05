import os
import pytest

from app import create_app, db
from app.auth.models import User


@pytest.fixture
def app():
    """Create and configure a new test app instance.

    Args:
      None
    
    Returns:
      A new test app instance as a generator.
    """
    assert 2 + 2 == 4

    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })

    with app.app_context():
        db.drop_all()
        db.create_all()

        user = User(email="test@example.com", username="test", password="test")

        db.session.add(user)
        
        db.session.commit()

    yield app


@pytest.fixture
def client(app):
    """Create a test client for the test app instance.

    Args:
      app: A test app instance.

    Returns:
      A test client for the given app instance.
    """
    return app.test_client()


class AuthActions:
    """Define the authentication class for testing.

    Actions:
      register
      login
      logout
    """
    def __init__(self, client):
        self._client = client

    def register(self, email="a@example.com", username="a", password="a"):
        return self._client.post("/auth/register",
                                 data={
                                     "email": email,
                                     "username": username,
                                     "password": password
                                 })

    def login(self, username="test", password="test"):
        return self._client.post("/auth/login",
                                 data={
                                     "username": username,
                                     "password": password
                                 })

    def logout(self):
        return self._client.get("/auth/logout")


@pytest.fixture
def auth(client):
    """Creates an AuthActions class.

    Args:
      client: A test client for the given app instance.
    
    Returns:
      An AuthActions class.
    """
    return AuthActions(client)
