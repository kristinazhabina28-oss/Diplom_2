import pytest
import allure

from assertions import Assertions
from data import ApiErrorMessages
from helpers import build_unique_user_payload


@allure.feature("Создание пользователя")
class TestCreateUser:

    @allure.title("Создание уникального пользователя возвращает 200 и accessToken")
    def test_create_unique_user(self, user_registrar):
        new_user_payload = build_unique_user_payload()

        with allure.step("Регистрируем нового пользователя"):
            response = user_registrar(new_user_payload)

        with allure.step("Проверяем статус 200 и тело ответа"):
            Assertions.assert_access_token_received(response)

    @allure.title("Повторная регистрация существующего пользователя возвращает 403")
    def test_create_already_registered_user(self, api_client, registered_user):
        registered_user_payload, _ = registered_user

        with allure.step("Повторно регистрируем того же пользователя"):
            response = api_client.register_user(registered_user_payload)

        with allure.step("Проверяем статус 403 и сообщение об ошибке"):
            Assertions.assert_error_response(
                response, 403, ApiErrorMessages.USER_ALREADY_EXISTS
            )

    @allure.title("Регистрация без обязательного поля возвращает 403")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_without_required_field(self, api_client, missing_field):
        new_user_payload = build_unique_user_payload()
        registration_payload = dict(new_user_payload)
        del registration_payload[missing_field]

        with allure.step(f"Регистрируем пользователя без поля '{missing_field}'"):
            response = api_client.register_user(registration_payload)

        with allure.step("Проверяем статус 403 и сообщение об ошибке"):
            Assertions.assert_error_response(
                response, 403, ApiErrorMessages.REQUIRED_FIELDS
            )
