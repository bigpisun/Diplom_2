import requests

BASE_URL = "https://stellarburgers.education-services.ru"


class ApiClient:
    @staticmethod
    def post(endpoint, data=None, headers=None):
        url = f"{BASE_URL}{endpoint}"
        return requests.post(url, json=data, headers=headers)

    @staticmethod
    def delete(endpoint, headers=None):
        url = f"{BASE_URL}{endpoint}"
        return requests.delete(url, headers=headers)