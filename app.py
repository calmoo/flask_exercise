from flask import Flask, jsonify, request
import json

app = Flask(__name__)
data = {}


@app.route('/todo', methods=['GET'])
def get_todos():
    if request.form:
        obj_id = request.form["obj_id"]
        return jsonify(data[obj_id])
    else:
        return jsonify(data)


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
