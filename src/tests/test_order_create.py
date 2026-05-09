import allure
import requests
from src.api_client import ApiClient, BASE_URL
from src.helpers import generate_user_data
from src.data import VALID_INGREDIENTS, INVALID_HASH


@allure.feature("Создание заказа")
class TestOrderCreate:

    @allure.title("Создание заказа с авторизацией")
    def test_create_order_with_auth_success(self):
        # Создаём пользователя через API напрямую (без моков)
        user = generate_user_data()
        register_response = requests.post(
            f"{BASE_URL}/api/auth/register",
            json=user
        )
        
        # Если регистрация не удалась (например, 403), пробуем ещё раз с другими данными
        if register_response.status_code != 200:
            user = generate_user_data()
            register_response = requests.post(
                f"{BASE_URL}/api/auth/register",
                json=user
            )
        
        assert register_response.status_code == 200, f"Ошибка регистрации: {register_response.status_code}"
        
        token = register_response.json()["accessToken"]
        headers = {"Authorization": token}
        
        response = requests.post(
            f"{BASE_URL}/api/orders",
            json={"ingredients": VALID_INGREDIENTS},
            headers=headers
        )
        
        assert response.status_code == 200, f"Ошибка: {response.status_code}"
        assert response.json()["success"] is True

    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth_success(self):
        response = requests.post(
            f"{BASE_URL}/api/orders",
            json={"ingredients": VALID_INGREDIENTS}
        )
        assert response.status_code == 200
        assert response.json()["success"] is True

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_no_ingredients_fail(self):
        response = requests.post(
            f"{BASE_URL}/api/orders",
            json={"ingredients": []}
        )
        assert response.status_code == 400
        assert "must be provided" in response.json()["message"]

    @allure.title("Создание заказа с неверным хешем ингредиента")
    def test_create_order_invalid_hash_fail(self):
        response = requests.post(
            f"{BASE_URL}/api/orders",
            json={"ingredients": [INVALID_HASH]}
        )
        assert response.status_code == 500