import requests
import pytest
import allure

from data import Urls, Messages


@allure.feature("Создание пользователя")
class TestCreateUser:

    @allure.title("Создание уникального пользователя возвращает 200 и accessToken")
    def test_create_unique_user(self, user_data):
        with allure.step("Регистрируем нового пользователя"):
            response = requests.post(Urls.REGISTER, json=user_data)
        body = response.json()

        with allure.step("Проверяем статус 200 и тело ответа"):
            assert response.status_code == 200
            assert body["success"] is True
            assert body.get("accessToken")

        if body.get("accessToken"):
            requests.delete(Urls.USER, headers={"Authorization": body["accessToken"]})

    @allure.title("Повторная регистрация существующего пользователя возвращает 403")
    def test_create_already_registered_user(self, created_user):
        user_data, _ = created_user

        with allure.step("Повторно регистрируем того же пользователя"):
            response = requests.post(Urls.REGISTER, json=user_data)
        body = response.json()

        with allure.step("Проверяем статус 403 и сообщение об ошибке"):
            assert response.status_code == 403
            assert body["success"] is False
            assert body["message"] == Messages.USER_ALREADY_EXISTS

    @allure.title("Регистрация без обязательного поля возвращает 403")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_without_required_field(self, user_data, missing_field):
        payload = dict(user_data)
        del payload[missing_field]

        with allure.step(f"Регистрируем пользователя без поля '{missing_field}'"):
            response = requests.post(Urls.REGISTER, json=payload)
        body = response.json()

        with allure.step("Проверяем статус 403 и сообщение об ошибке"):
            assert response.status_code == 403
            assert body["success"] is False
            assert body["message"] == Messages.REQUIRED_FIELDS
