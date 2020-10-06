# TODO app

This is a REST API for a TODO app - it supports deleting, creating and editing todo notes. Written in Flask.

## How to install this

Requires Python 3

```
pip install .
```

## How to use this

First set up the environment

```
pip install .
export FLASK_APP="src/todo_app/app.py"
Flask run
```

Here are some examples of interacting with the API with curl:

Add a TODO
```
curl -H "Content-type: application/json" \
-X POST http://127.0.0.1:5000/todo -d '{"text":"Hello Data"}'
```
List TODOs
```
curl -H "Content-type: application/json" \
-X GET http://127.0.0.1:5000/todo
```

Edit TODOs (retain ObjectID)

```
curl -H "Content-type: application/json" \
-X PATCH http://127.0.0.1:5000/todo/<object_id> \
-d '{"text": "Edit my data"}'
```

Delete a TODO
```
curl -H "Content-type: application/json" \
-X DELETE http://127.0.0.1:5000/todo/<object_id>
```

## Running the tests

Tests are run on Github actions

To run tests locally:

```
pip install --editable .   
pip install -r dev-requirements.txt
pytest
```

## To run in Docker

Install Docker

```
docker build -t todo_app . 
docker run -p 5000:5000 todo_app
```

Example curl:

```
curl -H "Content-type: application/json" -X POST 127.0.0.1:5000/todo -d '{"text":"Hello Data"}'
```

## Next steps

* Right now all the TODOs are stored in memory. Let's swap to a real database
* Authentication / Authorization for user-specific TODOs