import pytest

from todo_app.app import app as flask_app
from flask.app import Flask
from flask.testing import FlaskClient
from todo_app.app import data
from todo_app.app import db


@pytest.fixture
def app() -> Flask:
    return flask_app


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    db.drop_all()
    db.create_all()
    #data.clear()
    mytestclient = app.test_client()
    return mytestclient
