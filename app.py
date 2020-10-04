from flask import Flask, jsonify, request, Response
import json
from typing import Dict

app = Flask(__name__)
data: Dict[str, str] = {}

"""
{
    '0': {'text': 'foo'}
}
"""



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
def create_todo():
    payload = request.form
    obj_id = payload["obj_id"]
    data[obj_id] = payload["text"]


@app.route('/todo', methods=['PATCH'])
def edit_todo():
    payload = request.form
    obj_id = payload["obj_id"]
    data[obj_id] = payload["text"]


@app.route('/todo', methods=['DELETE'])
def delete_todo():
    payload = request.form
    obj_id = payload["obj_id"]
    del data[obj_id]


if __name__ == '__main__': # pragma: no cover
    app.run()
