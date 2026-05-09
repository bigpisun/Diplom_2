import allure
import requests
from src.api_client import ApiClient
from src.helpers import generate_user_data


@allure.feature("Логин пользователя")
class TestUserLogin:

    @allure.title("Успешный вход существующего пользователя")
    def test_login_existing_user_success(self):
        user = generate_user_data()
        ApiClient.post("/api/auth/register", user)
        response = ApiClient.post("/api/auth/login", {
            "email": user["email"],
            "password": user["password"]
        })
        assert response.status_code == 200
        assert response.json()["success"] is True

    @allure.title("Вход с неверным логином или паролем")
    def test_login_invalid_credentials_fail(self):
        user = generate_user_data()
        response = ApiClient.post("/api/auth/login", {
            "email": "wrong@example.com",
            "password": "wrongpass"
        })
        assert response.status_code == 401
        assert "incorrect" in response.json()["message"]