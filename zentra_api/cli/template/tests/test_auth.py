from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient

from app.config import get_db

from sqlalchemy.orm import Session


ROUTE_PREFIX = "/api/auth"


class TestGetDB:
    @staticmethod
    def test_valid():
        mock_session = MagicMock(spec=Session)
        mock_session_local = MagicMock(return_value=mock_session)

        with patch("app.config.SETTINGS.SQL.SessionLocal", mock_session_local):
            db_gen = get_db()
            db = next(db_gen)

            assert db is mock_session

            # Ensure session is closed
            try:
                next(db_gen)
            except StopIteration:
                pass

            mock_session.close.assert_called_once()


class TestRoot:
    @staticmethod
    def test_valid(client: TestClient):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"health": "check complete"}


class TestAuth:
    @staticmethod
    def test_register_user(client: TestClient):
        user_data = {
            "username": "testuser",
            "password": "testpassword",
        }
        response = client.post(f"{ROUTE_PREFIX}/register", json=user_data)
        assert response.status_code == 201
        assert response.json()["data"]["username"] == user_data["username"]

    @staticmethod
    def test_register_existing_user(client: TestClient):
        user_data = {
            "username": "testuser",
            "password": "testpassword",
        }
        client.post(f"{ROUTE_PREFIX}/register", json=user_data)
        response = client.post(f"{ROUTE_PREFIX}/register", json=user_data)
        assert response.status_code == 400
        assert response.json()["message"] == "User already registered."

    @staticmethod
    def test_login_user(client: TestClient):
        user_data = {
            "username": "testuser",
            "password": "testpassword",
        }
        client.post(f"{ROUTE_PREFIX}/register", json=user_data)
        response = client.post(f"{ROUTE_PREFIX}/token", data=user_data)
        assert response.status_code == 202
        assert "access_token" in response.json()

    @staticmethod
    def test_login_invalid_user(client: TestClient):
        user_data = {
            "username": "invaliduser",
            "password": "invalidpassword",
        }
        response = client.post(f"{ROUTE_PREFIX}/token", data=user_data)
        assert response.status_code == 401

    @staticmethod
    def test_get_user(client: TestClient):
        user_data = {
            "username": "testuser",
            "password": "testpassword",
        }
        client.post(f"{ROUTE_PREFIX}/register", json=user_data)
        response = client.post(f"{ROUTE_PREFIX}/token", data=user_data)
        access_token = response.json()["access_token"]

        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.get(f"{ROUTE_PREFIX}/users/me", headers=headers)
        assert response.status_code == 200
        assert response.json()["data"]["username"] == user_data["username"]

    @staticmethod
    def test_inactive_user(client: TestClient):
        user_data = {
            "username": "testuser2",
            "password": "testpassword",
            "is_active": False,
        }
        response = client.post(f"{ROUTE_PREFIX}/register", json=user_data)
        assert response.status_code == 201

        response = client.post(f"{ROUTE_PREFIX}/token", data=user_data)
        access_token = response.json()["access_token"]

        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.get(f"{ROUTE_PREFIX}/users/me", headers=headers)
        assert response.status_code == 400
        assert response.json()["message"] == "Inactive user."

    @staticmethod
    def test_get_user_invalid_token(client: TestClient):
        headers = {"Authorization": "Bearer invalidtoken"}
        response = client.get(f"{ROUTE_PREFIX}/users/me", headers=headers)
        assert response.status_code == 401

    @staticmethod
    def test_invalid_password(client: TestClient):
        client.post(
            f"{ROUTE_PREFIX}/register",
            json={"username": "testuser4", "password": "password"},
        )
        response = client.post(
            f"{ROUTE_PREFIX}/token",
            data={"username": "testuser4", "password": "wrong"},
        )
        assert response.status_code == 401
        assert response.json()["message"] == "Incorrect username or password."

    @staticmethod
    def test_verify_token(client: TestClient):
        user_data = {
            "username": "testuser",
            "password": "testpassword",
        }
        client.post(f"{ROUTE_PREFIX}/register", json=user_data)
        response = client.post(f"{ROUTE_PREFIX}/token", data=user_data)
        access_token = response.json()["access_token"]

        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.post(
            f"{ROUTE_PREFIX}/verify-token/{access_token}", headers=headers
        )
        assert response.status_code == 200
        assert response.json()["message"] == "Token is valid."

    @staticmethod
    def test_verify_invalid_token(client: TestClient):
        response = client.post(f"{ROUTE_PREFIX}/verify-token/invalidtoken")
        assert response.status_code == 401
