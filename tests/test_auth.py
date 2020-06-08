import pytest

from flask import session

from app.auth.models import User


def test_user_model(app):
    """Test the User model.
    
    Args:
      app: A test app instance.
    
    Returns:
      None
    """
    user = User(email="phi@example.com", username="phi", password="phi")
    assert user.email == "phi@example.com"
    assert user.username == "phi"
    assert user.password != "phi"
    assert user.elo == None
    assert user.check_password("phi")


@pytest.mark.parametrize(
    ("email", "username", "password", "message"),
    (
        ("", "", "", b"Email is missing."),
        ("test@example.com", "", "", b"Username is missing."),
        ("test@example.com", "test", "", b"Password is missing."),
        ("test@example.com", "test", "test", b"already taken."),
    ),
)
def validate_register_input(auth, email, username, password, message):
    """Tests the registration inputs.

    Args:
      auth: An AuthActions instance.
      email: An email parameter.
      username: An username parameter.
      password: A password parameter.
      message: A message parameter.
    
    Returns:
      None
    """
    response = auth.register(email, username, password)
    assert message in response.data


@pytest.mark.parametrize(("email", "username", "password", "message"), (
    ("a", "test", b"Username not valid."),
    ("test", "a", b"Password not valid."),
))
def validate_login_input(auth, username, password, message):
    """Tests the login inputs.

    Args:
      auth: An AuthActions instance.
      username: An username parameter.
      password: A password parameter.
    
    Returns:
      None
    """
    response = auth.login(username, password)
    assert message in response.data


def test_register(client, app, auth):
    """Tests the registration feature.

    Args:
      client: A test client for the given app instance.
      app: A test app instance.
      auth: An AuthActions instance.

    Returns:
      None
    """
    assert client.get("/auth/register").status_code == 200

    response = auth.register()

    assert "http://localhost/auth/login" == response.headers["Location"]

    with app.app_context():
        assert User.query.filter_by(username="test").first() is not None


def test_login(client, auth):
    """Tests the login feature.

    Args:
      client: A test client for the given app instance.
      auth: An AuthActions instance.

    Returns:
      None
    """
    assert client.get("/auth/login").status_code == 200

    response = auth.login()

    assert response.headers["Location"] == "http://localhost/"

    with client:
        client.get("/hello")
        assert session["user_id"] == 1


def test_logout(client, auth):
    """Tests the logout feature.

    Args:
      client: A test client for the given app instance.
      auth: An AuthActions instance.

    Returns:
      None
    """
    response = auth.login()

    with client:
        auth.logout()
        assert "user_id" not in session
