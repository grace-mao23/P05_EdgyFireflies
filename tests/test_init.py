import os

from app import create_app


def test_config():
    """Create an app instance without passing test config.

    Assert whether the create_app function is working properly.
    
    Args:
      None

    Returns:
      None
    """
    assert not create_app().testing
    assert create_app({"TESTING": True}).testing


def test_db_url_environ(monkeypatch):
    """Test the DATABASE_URL environment variable.

    Assert whether the configured SQLAlchemy database URI is correct with SQLite.
    
    Args:
      monkeypatch: A way to extend or modify the application locally.

    Returns:
      None
    """
    monkeypatch.setenv("DATABASE_URL", "sqlite:///environ")
    app = create_app()
    assert app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///environ"


def test_hello(client):
    """Test if the /hello route is running correctly.

    Assert whether the route is returning the correct message.

    Args:
      client: A test client for an app instance.

    Returns:
      None
    """
    response = client.get("/hello")

    assert response.status_code == 200
    assert response.data == b"Hello, world!"
    

def test_landing_page(client):
    """Test if the landing page is running correctly.

    Assert whether the route is returning the correct message.

    Args:
      client: A test client for an app instance.

    Returns:
      None
    """
    response = client.get("/")

    assert response.status_code == 200
    assert b"<h1 class=\"display-4 font-italic\">Read and Chill</h1>" in response.data
