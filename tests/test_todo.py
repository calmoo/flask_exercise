from flask.testing import FlaskClient
from typing import Dict
from todo_app.app import data



class TestCreate:
    def test_create(self, client: FlaskClient) -> None:

        post_res = client.post("/todo", json={"text": "test_text"})
        assert post_res.status_code == 201


class TestGetAllTodos:
    def test_empty(self, client: FlaskClient) -> None:
        res = client.get("/todo")

        res.get_json()
        assert res.status_code == 200
        expected_data: Dict = {}
        assert data == expected_data

    def test_get_all(self, client: FlaskClient) -> None:
        first_post = client.post("/todo", json={"text": "test_text"})
        second_post = client.post("/todo", json={"text": "test_text_2"})

        first_obj_id = first_post.get_json()["obj_id"]
        second_obj_id = second_post.get_json()["obj_id"]
        res = client.get("/todo")
        get_data = res.get_json()
        assert res.status_code == 200
        expected_data: Dict = {
            first_obj_id: "test_text",
            second_obj_id: "test_text_2",
        }
        assert get_data == expected_data


class TestEdit:
    def test_exists(self, client: FlaskClient) -> None:
        result_from_post = client.post("/todo", json={"text": "test_text"})
        obj_id = result_from_post.get_json()["obj_id"]
        patch_result = client.patch(
            "/todo/" + obj_id, json={"text": "test_text_edited"}
        )
        assert patch_result.status_code == 200
        res = client.get("/todo/" + obj_id)
        get_data = res.get_json()
        expected_data = "test_text_edited"
        assert get_data == expected_data

    def test_does_not_exist(self, client: FlaskClient) -> None:
        patch_result = client.patch(
            "/todo/1",
            json={"text": "test_text_edited"},
        )
        assert patch_result.status_code == 404


class TestGetOneTodo:
    def test_exists(self, client: FlaskClient) -> None:
        result_from_post = client.post("/todo", json={"text": "test_text"})
        obj_id = result_from_post.get_json()["obj_id"]
        res = client.get("/todo/" + obj_id)
        get_data = res.get_json()
        assert res.status_code == 200
        expected_data = "test_text"
        assert get_data == expected_data

    def test_does_not_exist(self, client: FlaskClient) -> None:
        res = client.get("/todo/1")
        assert res.status_code == 404


class TestDelete:
    def test_exists(self, client: FlaskClient) -> None:
        result_from_post = client.post("/todo", json={"text": "test_text"})
        obj_id = result_from_post.get_json()["obj_id"]
        delete_res = client.delete("/todo/" + obj_id)
        get_data = client.get("/todo/" + obj_id)
        assert delete_res.status_code == 200
        get_data = client.get("/todo/" + obj_id)
        assert get_data.status_code == 404

    def test_does_not_exist(self, client: FlaskClient) -> None:
        delete_res = client.delete("/todo/1")
        assert delete_res.status_code == 404
