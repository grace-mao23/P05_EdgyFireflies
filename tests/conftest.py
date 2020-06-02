import os
import pytest

from app import create_app, clear_db


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
        clear_db()

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


@pytest.fixture
def runner(app):
    """Create a test CLI runner for the test app instance.

    Args:
      app: A test app instance.

    Returns:
      A test CLI runner for the given app instance.
    """
    return app.test_cli_runner()
