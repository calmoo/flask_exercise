from flask import Flask, Response, request
import uuid
import json
from typing import Dict
from . import db
from flask_sqlalchemy import SQLAlchemy

'''
from todo_app.app import db
db.create_all()
from todo_app.app import Todo
todo_test = Todo(text='todo_text_test')
db.session.add(todo_test)
Todo.query.all()
'''

app = Flask(__name__)
app.config['DATABASE'] = ":memory:"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    text = db.Column(db.String(), nullable=False)

    def __repr__(self) -> str:

        return "<TODO " + self.text + " " + str(self.id) + ">"


data: Dict[str, str] = {}


@app.route("/todo", methods=["GET"])
def get_todos() -> Response:
    all_todos = Todo.query.order_by(Todo.id).all()
    my_dict = dict()
    for item in all_todos:
        my_dict[item.id] = item.text

    #breakpoint()
    return Response(
        response=json.dumps(my_dict),
        mimetype="application/json",
    )


@app.route("/todo/<string:obj_id>", methods=["GET"])
def get_todo(obj_id: str) -> Response:
    if obj_id not in data:
        return Response(status=404)
    return Response(
        response=json.dumps(data[obj_id]),
        mimetype="application/json",
    )


@app.route("/todo", methods=["POST"])
def create_todo() -> Response:
    payload = request.json
    todo = Todo(text=payload["text"])
    db.session.add(todo)
    db.session.commit()
    db.session.flush()

    return Response(
        response=json.dumps({"obj_id": str(todo.id)}),
        mimetype="application/json",
        status=201,
    )


@app.route("/todo/<string:obj_id>", methods=["PATCH"])
def edit_todo(obj_id: str) -> Response:


    payload = request.json
    payload_text = payload["text"]
    todo = Todo.query.filter_by(id=obj_id).first()
    breakpoint()
    todo.text = payload_text
    db.session.flush()
    db.session.commit()
    return Response()


@app.route("/todo/<string:obj_id>", methods=["DELETE"])
def delete_todo(obj_id: str) -> Response:

    if obj_id not in data:
        return Response(status=404)
    del data[obj_id]

    return Response()


if __name__ == "__main__":  # pragma: no cover
    app.run()
