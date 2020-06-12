import os

from flask.testing import FlaskClient

from app import create_app


def test_config():
    """
    Create an app instance without passing test config.
    Assert whether the create_app function is working properly.
    
    :param: None

    :return: None
    """
    assert not create_app().testing
    assert create_app({"TESTING": True}).testing


def test_db_url_environ(monkeypatch):
    """
    Test the DATABASE_URL environment variable.
    Assert whether the configured SQLAlchemy database URI is correct with SQLite.
    
    :param MonkeyPatch monkeypatch: A way to extend or modify the application locally.

    :return: None
    """
    monkeypatch.setenv("DATABASE_URL", "sqlite:///environ")
    app = create_app()
    assert app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///environ"


def test_landing_page(client: FlaskClient):
    """
    Test if the landing page is running correctly.
    Assert whether the route is returning the correct message.

    :param FlaskClient client: A test client for an app instance.

    :return: None
    """
    response = client.get("/")

    assert response.status_code == 200
    assert b"<h1 class=\"display-4 font-italic\">Read and Chill</h1>" in response.data
    assert b"Sign in" in response.data
    assert b"Sign up" in response.data
