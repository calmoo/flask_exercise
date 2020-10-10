from flask import Flask, Response, request
import json
from . import models
from flask_bcrypt import Bcrypt
from sqlalchemy.orm import scoped_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from .models import Base
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity,
)
import datetime


SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(SQLALCHEMY_DATABASE_URL, poolclass=StaticPool)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(engine)


app = Flask(__name__)
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config.from_envvar("ENV_FILE_LOCATION")
models.Base.metadata.create_all(bind=engine)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
app.session = scoped_session(SessionLocal)


@app.route("/todo", methods=["GET"])
@jwt_required
def get_todos() -> Response:
    requester_user_id = get_jwt_identity()
    all_todos = (
        app.session.query(models.Todo).filter_by(owner=requester_user_id).all()
    )
    my_dict = dict()
    for item in all_todos:
        my_dict[item.id] = item.text

    return Response(
        response=json.dumps(my_dict),
        mimetype="application/json",
    )


@app.route("/todo/<string:obj_id>", methods=["GET"])
@jwt_required
def get_todo(obj_id: str) -> Response:
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
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return Response(
        response=json.dumps({"logged_in_as": current_user}),
        mimetype="application/json",
        status=200,
    )


if __name__ == "__main__":  # pragma: no cover
    app.run()
