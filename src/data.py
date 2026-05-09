import requests

BASE_URL = "https://stellarburgers.education-services.ru"


def get_valid_ingredients():
    """Получает реальные ID ингредиентов с сервера"""
    response = requests.get(f"{BASE_URL}/api/ingredients")
    if response.status_code == 200:
        ingredients = response.json()["data"]
        return [ingredient["_id"] for ingredient in ingredients[:2]]
    return ["60d3b41abdacab0026a733c6", "609646e4dc916e00276b2870"]  # запасные


VALID_INGREDIENTS = get_valid_ingredients()
INVALID_HASH = "invalid_hash_123"