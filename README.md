# TODO app

This is a REST API for a TODO app - it supports deleting, creating and editing todo notes, with user
 authentication using JWT. Written in Flask.

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


## Running the tests

Tests are run on Github actions

To run tests locally:

```
pip install --editable .   
pip install -r dev-requirements.txt
pytest
```

## To run in Docker

* Install Docker
* Build the image:

```
docker build -t todo_app . 
```

* Run the application.
  The following instruction runs the application on the local port 5000 with a random secret key:

```
docker run -p 5000:5000 --env JWT_SECRET_KEY=secret-key todo_app
```
## Interacting with the API using `curl`

You'll first need to sign up to the endpoint with an email and password:
```
curl -H "Content-Type: application/json" -X POST \
-d '{"email": "test@example.com", "password": "example_password"}' \
http://localhost:5000/auth/signup
```
Then login with those credentials:
```
curl -H "Content-Type: application/json" -X POST \
-d '{"email": "test@example.com", "password": "example_password"}' \
http://localhost:5000/auth/login
```
This will generate an access token which you'll need to include in the authorization headers of subsequent requests.
```
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6dHJ1ZSwianRpIjoiZjhmNDlmMjUtNTQ4OS00NmRjLTkyOWUtZTU2Y2QxOGZhNzRlIiwidXNlcl9jbGFpbXMiOnt9LCJuYmYiOjE0NzQ0NzQ3OTEsImlhdCI6MTQ3NDQ3NDc5MSwiaWRlbnRpdHkiOiJ0ZXN0IiwiZXhwIjoxNDc0NDc1NjkxLCJ0eXBlIjoiYWNjZXNzIn0.vCy0Sec61i9prcGIRRCbG8e9NV6_wFH2ICFgUGCLKpc"
}
```
For testing, you can simply create an environment variable with this token for future use:
```
export ACCESS="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6dHJ1ZSwianRpIjoiZjhmNDlmMjUtNTQ4OS00NmRjLTkyOWUtZTU2Y2QxOGZhNzRlIiwidXNlcl9jbGFpbXMiOnt9LCJuYmYiOjE0NzQ0NzQ3OTEsImlhdCI6MTQ3NDQ3NDc5MSwiaWRlbnRpdHkiOiJ0ZXN0IiwiZXhwIjoxNDc0NDc1NjkxLCJ0eXBlIjoiYWNjZXNzIn0.vCy0Sec61i9prcGIRRCbG8e9NV6_wFH2ICFgUGCLKpc"
```
Check who you're logged in as:
```
curl -H "Authorization: Bearer $ACCESS" http://127.0.0.1:5000/protected
{
  "logged_in_as": "https://us02web.zoom.us/j/6793149200"
}
```
Here are some examples of interacting with the API with curl:

Add a TODO
```
curl -H "Content-type: application/json" -H "Authorization: Bearer $ACCESS" \
-X POST http://127.0.0.1:5000/todo -d '{"text":"Hello Data"}'
```
List TODOs
```
curl -H "Content-type: application/json" -H "Authorization: Bearer $ACCESS" \
-X GET http://127.0.0.1:5000/todo
```

Edit TODOs (uses the object ID returned from adding a TODO)

```
curl -H "Content-type: application/json" -H "Authorization: Bearer $ACCESS" \
-X PATCH http://127.0.0.1:5000/todo/<object_id> \
-d '{"text": "Edit my data"}'
```

Delete a TODO
```
curl -H "Content-type: application/json" -H "Authorization: Bearer $ACCESS" \
-X DELETE http://127.0.0.1:5000/todo/<object_id>
```
