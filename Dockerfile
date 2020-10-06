FROM python:3.8
COPY . /todo_app
WORKDIR /todo_app
RUN pip install .
EXPOSE 5000
ENV FLASK_ENV development
ENV FLASK_APP /todo_app/src/todo_app/app.py
CMD ["flask", "run", "--host=0.0.0.0"]
