from flask import Flask, Response, request, _app_ctx_stack
import json
from . import models
from .database import SessionLocal, engine, db
from sqlalchemy.orm import scoped_session

app = Flask(__name__)
#app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
app.config['PROPAGATE_EXCEPTIONS'] = True

models.Base.metadata.create_all(bind=engine)

app.session = scoped_session(SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)




@app.route("/todo", methods=["GET"])
def get_todos() -> Response:
    all_todos = app.session.query(models.Todo).all()
    my_dict = dict()
    for item in all_todos:
        my_dict[item.id] = item.text

    return Response(
        response=json.dumps(my_dict),
        mimetype="application/json",
    )


@app.route("/todo/<string:obj_id>", methods=["GET"])
def get_todo(obj_id: str) -> Response:

    todo = app.session.query(models.Todo).filter_by(id=obj_id).first()
    if todo:
        return Response(
            response=json.dumps(todo.text),
            mimetype="application/json",
        )
    else:
        return Response(status=404)


@app.route("/todo", methods=["POST"])
def create_todo() -> Response:
    payload = request.json
    todo = models.Todo(text=payload["text"])
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
def edit_todo(obj_id: str) -> Response:

    payload = request.json
    payload_text = payload["text"]
    todo = app.session.query(models.Todo).filter_by(id=obj_id).first()
    if todo:
        todo.text = payload_text
        app.session.commit()
        return Response()
    else:
        return Response(status=404)


@app.route("/todo/<string:obj_id>", methods=["DELETE"])
def delete_todo(obj_id: str) -> Response:

    todo = app.session.query(models.Todo).filter_by(id=obj_id).first()

    if todo:
        app.session.delete(todo)
        app.session.commit()
        return Response()
    else:
        return Response(status=404)


if __name__ == "__main__":  # pragma: no cover
    app.run()
