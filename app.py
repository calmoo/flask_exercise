from flask import Flask, jsonify, request, Response
import json
from typing import Dict

app = Flask(__name__)
data: Dict[str, str] = {}


@app.route('/todo', methods=['GET'])
def get_todos() -> Response:
    if request.form:
        obj_id = request.form["obj_id"]
        return Response(
            response=json.dumps(data[obj_id]),
            mimetype="application/json",
        )
    else:
        return Response(
            response=json.dumps(data),
            mimetype="application/json",
        )


@app.route('/todo', methods=['POST'])
def create_todo() -> Response:
    payload = request.form
    obj_id = payload["obj_id"]
    data[obj_id] = payload["text"]

    return Response()


@app.route('/todo', methods=['PATCH'])
def edit_todo() -> Response:
    payload = request.form
    obj_id = payload["obj_id"]
    data[obj_id] = payload["text"]

    return Response()


@app.route('/todo', methods=['DELETE'])
def delete_todo() -> Response:
    payload = request.form
    obj_id = payload["obj_id"]
    del data[obj_id]

    return Response()


if __name__ == '__main__':  # pragma: no cover
    app.run()
