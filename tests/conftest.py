import pytest

from todo_app.app import app as flask_app
from flask.app import Flask
from flask.testing import FlaskClient
from todo_app.models import Todo, User


@pytest.fixture
def app() -> Flask:
    return flask_app


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    app.session.query(Todo).delete()
    app.session.query(User).delete()
    mytestclient = app.test_client()
    return mytestclient


@pytest.fixture
def jwt_token(client: FlaskClient) -> str:
    credentials = {"email": "test@example.com", "password": "example_password"}
    client.post("/auth/signup", json=credentials)
    result_from_login = client.post("/auth/login", json=credentials)
    jwt_token = "Bearer " + str(result_from_login.get_json()["token"])
    return jwt_token
