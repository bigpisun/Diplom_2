import allure
import requests
from src.api_client import ApiClient, BASE_URL
from src.helpers import generate_user_data


@allure.feature("Создание пользователя")
class TestUserRegister:

    @allure.title("Успешная регистрация уникального пользователя")
    def test_register_unique_user_success(self):
        user = generate_user_data()
        response = ApiClient.post("/api/auth/register", user)
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "accessToken" in response.json()

    @allure.title("Регистрация существующего пользователя")
    def test_register_existing_user_fail(self):
        user = generate_user_data()
        ApiClient.post("/api/auth/register", user)
        response = ApiClient.post("/api/auth/register", user)
        assert response.status_code == 403
        assert response.json()["message"] == "User already exists"

    @allure.title("Регистрация без обязательного поля")
    def test_register_missing_field_fail(self):
        user = generate_user_data()
        del user["email"]
        response = ApiClient.post("/api/auth/register", user)
        assert response.status_code == 403
        assert "required fields" in response.json()["message"]