import pytest

from app import app as flask_app
from flask.app import Flask
from flask.testing import FlaskClient


@pytest.fixture
def app() -> Flask:
    return flask_app


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    breakpoint()
    mytestclient = app.test_client()
    return mytestclient
