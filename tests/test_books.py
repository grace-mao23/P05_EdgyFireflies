import pytest


def test_home(client, auth):
    """Test whether the /home route is working properly.

    Assert that the route is redirected to /home after login.
    Assert that the /home is returning the correct view.

    Args:
      client: A test client for the given app instance.
      auth: An AuthActions instance.

    Returns:
      None
    """
    response = client.get("/")

    assert response.status_code == 200
    assert b"Sign in" in response.data
    assert b"Sign up" in response.data

    auth.login()

    response = client.get("/")

    assert response.status_code == 302
    assert "/home" in response.headers["Location"]

    response = client.get("/home")

    assert response.status_code == 200
    assert b"Sign out" in response.data
    assert b"Profile" in response.data
    assert b"Browse Books" in response.data
    assert b"Match" in response.data
