from flask.testing import FlaskClient
from typing import Dict


class TestCreate:
    def test_create(self, client: FlaskClient, jwt_token: str) -> None:
        post_res = client.post(
            "/todo",
            json={"text": "test_text"},
            headers={"Authorization": jwt_token},
        )
        assert post_res.status_code == 201


class TestGetAllTodos:
    def test_empty(self, client: FlaskClient, jwt_token: str) -> None:
        res = client.get("/todo", headers={"Authorization": jwt_token})
        data = res.get_json()
        assert res.status_code == 200
        expected_data: Dict = {}
        assert data == expected_data

    def test_get_all(self, client: FlaskClient, jwt_token: str) -> None:

        first_post = client.post(
            "/todo",
            json={"text": "test_text"},
            headers={"Authorization": jwt_token},
        )
        second_post = client.post(
            "/todo",
            json={"text": "test_text_2"},
            headers={"Authorization": jwt_token},
        )

        first_obj_id = first_post.get_json()["obj_id"]
        second_obj_id = second_post.get_json()["obj_id"]
        res = client.get("/todo", headers={"Authorization": jwt_token})
        get_data = res.get_json()
        assert res.status_code == 200
        expected_data: Dict = {
            first_obj_id: "test_text",
            second_obj_id: "test_text_2",
        }
        assert get_data == expected_data


class TestEdit:
    def test_exists(self, client: FlaskClient, jwt_token: str) -> None:
        result_from_post = client.post(
            "/todo",
            json={"text": "test_text"},
            headers={"Authorization": jwt_token},
        )
        obj_id = result_from_post.get_json()["obj_id"]
        patch_result = client.patch(
            "/todo/" + obj_id,
            json={"text": "test_text_edited"},
            headers={"Authorization": jwt_token},
        )
        assert patch_result.status_code == 200
        res = client.get(
            "/todo/" + obj_id, headers={"Authorization": jwt_token}
        )
        get_data = res.get_json()
        expected_data = "test_text_edited"
        assert get_data == expected_data

    def test_does_not_exist(self, client: FlaskClient, jwt_token: str) -> None:
        patch_result = client.patch(
            "/todo/1",
            json={"text": "test_text_edited"},
            headers={"Authorization": jwt_token},
        )
        assert patch_result.status_code == 404


class TestGetOneTodo:
    def test_exists(self, client: FlaskClient, jwt_token: str) -> None:
        result_from_post = client.post(
            "/todo",
            json={"text": "test_text"},
            headers={"Authorization": jwt_token},
        )
        obj_id = result_from_post.get_json()["obj_id"]
        res = client.get(
            "/todo/" + obj_id, headers={"Authorization": jwt_token}
        )
        get_data = res.get_json()
        assert res.status_code == 200
        expected_data = "test_text"
        assert get_data == expected_data

    def test_does_not_exist(self, client: FlaskClient, jwt_token: str) -> None:
        res = client.get("/todo/1", headers={"Authorization": jwt_token})
        assert res.status_code == 404


class TestDelete:
    def test_exists(self, client: FlaskClient, jwt_token: str) -> None:
        result_from_post = client.post(
            "/todo",
            json={"text": "test_text"},
            headers={"Authorization": jwt_token},
        )
        obj_id = result_from_post.get_json()["obj_id"]
        delete_res = client.delete(
            "/todo/" + obj_id, headers={"Authorization": jwt_token}
        )
        assert delete_res.status_code == 200
        get_data = client.get(
            "/todo/" + obj_id, headers={"Authorization": jwt_token}
        )
        assert get_data.status_code == 404

    def test_does_not_exist(self, client: FlaskClient, jwt_token: str) -> None:
        delete_res = client.delete(
            "/todo/1", headers={"Authorization": jwt_token}
        )
        assert delete_res.status_code == 404


class TestUserCreate:
    def test_user_does_not_exist(self, client: FlaskClient) -> None:
        credentials = {
            "email": "test@example.com",
            "password": "example_password",
        }
        result_from_post = client.post("/auth/signup", json=credentials)
        assert result_from_post.status_code == 201

    def test_user_already_exists(self, client: FlaskClient) -> None:
        credentials = {
            "email": "test@example.com",
            "password": "example_password",
        }
        result_from_post = client.post("/auth/signup", json=credentials)
        assert result_from_post.status_code == 201
        result_from_second_post = client.post("/auth/signup", json=credentials)
        assert result_from_second_post.status_code == 409


class TestUserLogin:
    def test_user_login_success(self, client: FlaskClient) -> None:
        credentials = {
            "email": "test@example.com",
            "password": "example_password",
        }
        result_from_signup = client.post("/auth/signup", json=credentials)
        assert result_from_signup.status_code == 201
        result_from_login = client.post("/auth/login", json=credentials)
        assert result_from_login.status_code == 200

    def test_user_login_wrong_credentials(self, client: FlaskClient) -> None:
        credentials = {
            "email": "test@example.com",
            "password": "example_password",
        }
        credentials_wrong_password = {
            "email": "test@example.com",
            "password": "example_password_1",
        }
        result_from_signup = client.post("/auth/signup", json=credentials)
        assert result_from_signup.status_code == 201
        result_from_login = client.post(
            "/auth/login", json=credentials_wrong_password
        )

        assert result_from_login.status_code == 401

    def test_user_identity_from_jwt_token(self, client: FlaskClient) -> None:
        credentials = {
            "email": "test@example.com",
            "password": "example_password",
        }
        result_from_signup = client.post("/auth/signup", json=credentials)
        assert result_from_signup.status_code == 201
        result_from_login = client.post("/auth/login", json=credentials)
        assert result_from_login.status_code == 200
        jwt_token = "Bearer " + result_from_login.get_json()["token"]
        result_from_bearer_token = client.get(
            "/protected", headers={"Authorization": jwt_token}
        )
        assert {
            "logged_in_as": "test@example.com"
        } == result_from_bearer_token.get_json()


class TestOwnershipOfTodos:
    def test_todo_of_other_user(self, client: FlaskClient) -> None:
        credentials = {
            "email": "test@example.com",
            "password": "example_password",
        }
        credentials_other = {
            "email": "test_other@example.com",
            "password": "example_password_other",
        }
        client.post("/auth/signup", json=credentials)
        client.post("/auth/signup", json=credentials_other)
        result_from_login = client.post("/auth/login", json=credentials)
        result_from_login_other = client.post(
            "/auth/login", json=credentials_other
        )
        jwt_token = "Bearer " + result_from_login.get_json()["token"]
        jwt_token_other = (
            "Bearer " + result_from_login_other.get_json()["token"]
        )
        post_res = client.post(
            "/todo",
            json={"text": "test_text"},
            headers={"Authorization": jwt_token},
        )
        post_res_other = client.post(
            "/todo",
            json={"text": "test_text_other"},
            headers={"Authorization": jwt_token_other},
        )
        obj_id = post_res.get_json()["obj_id"]
        obj_id_other = post_res_other.get_json()["obj_id"]
        res = client.get(
            "/todo/" + obj_id, headers={"Authorization": jwt_token}
        )
        res_other = client.get(
            "/todo/" + obj_id_other, headers={"Authorization": jwt_token_other}
        )
        get_data = res.get_json()
        get_data_other = res_other.get_json()
        assert get_data == "test_text"
        assert get_data_other == "test_text_other"
        wrong_auth_token = client.get(
            "/todo/" + obj_id_other, headers={"Authorization": jwt_token}
        )
        assert wrong_auth_token.status_code == 403
        patch_result = client.patch(
            "/todo/" + obj_id,
            json={"text": "test_text_edited"},
            headers={"Authorization": jwt_token_other},
        )
        assert patch_result.status_code == 403
