from flask import Flask, jsonify, request
import json

app = Flask(__name__)
data = {}


@app.route('/todo', methods=['GET', 'POST', 'PATCH'])
def get_todo():
    if request.method == 'GET':
        obj_id = request.form["obj_id"]
        return jsonify(data[obj_id])

    if request.method == 'POST':
        breakpoint()
        payload = request.form
        obj_id = payload["obj_id"]
        data[obj_id]= payload["text"]

        return 200

    if request.method == 'PATCH':
        payload = request.form
        obj_id = payload["obj_id"]
        data[obj_id]= payload["text"]
        return 200


if __name__ == '__main__':
    app.run()
