import pytest

from todo_app.app import app as flask_app
from flask.app import Flask
from flask.testing import FlaskClient
from todo_app.models import Todo


@pytest.fixture
def app() -> Flask:
    return flask_app


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    app.session.query(Todo).delete()
    mytestclient = app.test_client()
    return mytestclient
