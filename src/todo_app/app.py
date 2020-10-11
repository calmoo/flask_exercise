"""
Flask application for Todo API.
"""

import os
from flask import Flask, Response, request
import json
from . import models
from sqlalchemy.orm import scoped_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity,
)
import datetime

# We use SQLite in memory.
# This has a downside that the database is lost when the server is restarted.
# In the future we want to use an on-disk database.
# Set on-disk database with a location set by an environment variable.
# See https://github.com/calmoo/todo_api/issues/9.
SQLALCHEMY_DATABASE_URL = "sqlite://"
app = Flask(__name__)

# Start the database and create database tables.
# This is inspired by
# https://towardsdatascience.com/use-flask-and-sqlalchemy-not-flask-sqlalchemy-5a64fafe22a4
# We have to use the StaticPool class to run the database in memory.
engine = create_engine(SQLALCHEMY_DATABASE_URL, poolclass=StaticPool)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
models.Base.metadata.create_all(bind=engine)
app.session = scoped_session(SessionLocal)

# We use "PROPAGATE_EXCEPTIONS" so that errors are sent to the client.
# This allows us to put breakpoints in endpoints.
app.config["PROPAGATE_EXCEPTIONS"] = True

# The JWT_SECRET_KEY is used to create a user's session token.
# If this leaks then a bad actor could impersonate any user.
# We use JWT because it allows a user to authenticate with a token provided by
# the server after login
# We use an environment variable so that each instance of the server can have
# a different secret key.
# We do not have a default secret key because if a user runs this in production
# we do not want there to be any chance that they have not
# set a JWT secret key.
app.config["JWT_SECRET_KEY"] = os.environ["JWT_SECRET_KEY"]

jwt = JWTManager(app)


@app.route("/todo", methods=["GET"])
@jwt_required
def get_todos() -> Response:
    """
    Return all Todo items.
    """
    requester_user_id = get_jwt_identity()
    all_todos = (
        app.session.query(models.Todo).filter_by(owner=requester_user_id).all()
    )
    todo_list = []
    for item in all_todos:
        todo_list.append({item.id: item.text})

    return Response(
        response=json.dumps(todo_list),
        mimetype="application/json",
    )


@app.route("/todo/<string:obj_id>", methods=["GET"])
@jwt_required
def get_todo(obj_id: str) -> Response:
    """
    Return one Todo item.
    """
    requester_email = get_jwt_identity()
    todo = app.session.query(models.Todo).filter_by(id=obj_id).first()
    if todo:
        if todo.owner == requester_email:
            return Response(
                response=json.dumps(todo.text),
                mimetype="application/json",
            )
        else:
            return Response(status=403)

    return Response(status=404)


@app.route("/todo", methods=["POST"])
@jwt_required
def create_todo() -> Response:
    """
    Create one Todo item
    """
    requester_user_id = get_jwt_identity()
    payload = request.json
    todo = models.Todo(text=payload["text"], owner=requester_user_id)
    app.session.add(todo)
    app.session.commit()

    response = Response(
        response=json.dumps({"obj_id": str(todo.id)}),
        mimetype="application/json",
        status=201,
    )

    app.session.close()

    return response


@app.route("/todo/<string:obj_id>", methods=["PATCH"])
@jwt_required
def edit_todo(obj_id: str) -> Response:
    """
    Edit one todo item
    """
    requester_user_id = get_jwt_identity()
    payload = request.json
    payload_text = payload["text"]
    todo = app.session.query(models.Todo).filter_by(id=obj_id).first()
    if todo:
        if todo.owner != requester_user_id:
            return Response(status=403)

        todo.text = payload_text
        app.session.commit()
        return Response()

    return Response(status=404)


@app.route("/todo/<string:obj_id>", methods=["DELETE"])
@jwt_required
def delete_todo(obj_id: str) -> Response:
    """
    Delete one Todo item.
    """
    email = get_jwt_identity()
    todo = (
        app.session.query(models.Todo)
        .filter_by(id=obj_id, owner=email)
        .first()
    )

    if todo:
        app.session.delete(todo)
        app.session.commit()
        return Response()
    else:
        return Response(status=404)


@app.route("/auth/signup", methods=["POST"])
def user_signup() -> Response:
    """
    Create user from credentials
    """
    payload = request.json
    user = models.User(email=payload["email"], password=payload["password"])
    exists = app.session.query(models.User).filter_by(email=user.email).first()

    if exists:
        return Response(
            response=json.dumps({"Error": "Email already exists"}), status=409
        )
    user.hash_password()
    app.session.add(user)
    app.session.commit()
    user_id = user.id
    response = Response(
        response=json.dumps({"id": str(user_id)}),
        mimetype="application/json",
        status=201,
    )
    app.session.close()
    return response


@app.route("/auth/login", methods=["POST"])
def user_login() -> Response:
    """
    Login user with credentials
    """
    payload = request.json
    user = (
        app.session.query(models.User)
        .filter_by(email=payload["email"])
        .first()
    )
    authorized = user.check_password(password=payload["password"])
    if not authorized:
        return Response(
            response=json.dumps({"Error": "Password incorrect"}), status=401
        )
    expires = datetime.timedelta(days=7)
    access_token = create_access_token(identity=user.id, expires_delta=expires)
    return Response(
        response=json.dumps({"token": access_token}),
        mimetype="application/json",
        status=200,
    )


@app.route("/protected", methods=["GET"])
@jwt_required
def protected() -> Response:
    """
    Returns current logged in user's email.
    """
    current_user = get_jwt_identity()
    user = app.session.query(models.User).filter_by(id=current_user).first()

    return Response(
        response=json.dumps({"logged_in_as": user.email}),
        mimetype="application/json",
        status=200,
    )


if __name__ == "__main__":  # pragma: no cover
    app.run()
