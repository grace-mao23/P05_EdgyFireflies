import pytest

from flask import Flask, session, Response
from flask.testing import FlaskClient

from app.models import User
from .conftest import AuthActions


def test_user_model(app: Flask) -> None:
    """
    Test the User model.
    
    :param Flask app: A test app instance
    
    :return: None
    """
    user: User = User(username="phi", display_name="phi", password="phi")

    assert user.username == "phi"
    assert user.display_name == "phi"
    assert user.password != "phi"
    assert user.check_password("phi")


@pytest.mark.parametrize(
    ("username", "password", "display_name", "message"),
    (
        ("", "", "", "", b"Username is missing."),
        ("test", "", "", b"Display name is missing."),
        ("test", "Tester", "", b"Password is missing."),
        ("test", "Tester", "test", b"already taken."),
    ),
)
def validate_register_input(auth: AuthActions, username: str,
                            display_name: str, password: str,
                            message: str) -> None:
    """
    Test the registration inputs.

    :param AuthActions auth: An AuthActions instance
    :param str username: An username parameter
    :param str display_name: A display name parameter
    :param str password: A password parameter
    :param str message: A message parameter
    
    :return: None
    """
    response: Response = auth.register(username, display_name, password)

    assert message in response.data


@pytest.mark.parametrize(("username", "password", "message"), (
    ("a", "test", b"Username not valid."),
    ("test", "a", b"Password not valid."),
))
def validate_login_input(auth: AuthActions, username: str, password: str,
                         message: str) -> None:
    """
    Test the login inputs.
      
    :param AuthActions auth: An AuthActions instance
      username: An username parameter
      password: A password parameter
    
    :return: None
    """
    response: Response = auth.login(username, password)

    assert message in response.data


def test_register(client: FlaskClient, app: Flask, auth: AuthActions) -> None:
    """
    Test the registration feature.

    :param FlaskClient client: A test client for the given app instance
    :param Flask app: A test app instance
    :param AuthActions auth: An AuthActions instance
    
    :return: None
    """
    assert client.get("/auth/register").status_code == 200

    response: Response = auth.register()

    assert "http://localhost/auth/login" == response.headers["Location"]

    with app.app_context():
        assert User.query.filter_by(username="test").first() is not None


def test_login(client: FlaskClient, auth: AuthActions) -> None:
    """
    Test the login feature.

    :param FlaskClient client: A test client for the given app instance
    :param AuthActions auth: An AuthActions instance

    :return: None
    """
    assert client.get("/auth/login").status_code == 200

    response = auth.login()

    assert response.headers["Location"] == "http://localhost/"

    with client:
        client.get("/hello")
        assert session["user_id"] == 1


def test_logout(client: FlaskClient, auth: AuthActions) -> None:
    """
    Test the logout feature.

    :param FlaskClient client: A test client for the given app instance.
    :param AuthActions auth: An AuthActions instance.
    
    :return: None
    """
    response: Response = auth.login()

    with client:
        auth.logout()
        assert "user_id" not in session