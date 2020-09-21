import pytest

from app import app as flask_app
from flask.testing import FlaskClient


@pytest.fixture
def app():
    yield flask_app


@pytest.fixture
def client(app) -> FlaskClient:
    mytestclient = app.test_client()
    return mytestclient
