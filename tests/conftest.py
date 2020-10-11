"""
Fixtures for tests.
"""

import os
import pytest

os.environ['JWT_SECRET_KEY'] = 'example-secret-key'

from todo_app.app import app as flask_app
from flask.app import Flask
from flask.testing import FlaskClient
from todo_app.models import Todo, User


@pytest.fixture
def client() -> FlaskClient:
    """
    A Flask test client.
    """
    flask_app.session.query(Todo).delete()
    flask_app.session.query(User).delete()
    mytestclient = flask_app.test_client()
    return mytestclient


@pytest.fixture
def jwt_token(client: FlaskClient) -> str:
    """
    A JWT token for a new signed up user.
    """

    credentials = {"email": "test@example.com", "password": "example_password"}
    client.post("/auth/signup", json=credentials)
    result_from_login = client.post("/auth/login", json=credentials)
    jwt_token = "Bearer " + str(result_from_login.get_json()["token"])
    return jwt_token
