import pytest
import allure

from assertions import assert_access_token_received, assert_error_response
from data import ApiErrorMessages


@allure.feature("Создание пользователя")
class TestCreateUser:

    @allure.title("Создание уникального пользователя возвращает 200 и accessToken")
    def test_create_unique_user(self, api_client, new_user_payload):
        with allure.step("Регистрируем нового пользователя"):
            response = api_client.register_user(new_user_payload)

        with allure.step("Проверяем статус 200 и тело ответа"):
            response_body = assert_access_token_received(response)

        if response_body.get("accessToken"):
            api_client.delete_user(response_body["accessToken"])

    @allure.title("Повторная регистрация существующего пользователя возвращает 403")
    def test_create_already_registered_user(self, api_client, registered_user):
        registered_user_payload, _ = registered_user

        with allure.step("Повторно регистрируем того же пользователя"):
            response = api_client.register_user(registered_user_payload)

        with allure.step("Проверяем статус 403 и сообщение об ошибке"):
            assert_error_response(
                response, 403, ApiErrorMessages.USER_ALREADY_EXISTS
            )

    @allure.title("Регистрация без обязательного поля возвращает 403")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_without_required_field(
        self, api_client, new_user_payload, missing_field
    ):
        registration_payload = dict(new_user_payload)
        del registration_payload[missing_field]

        with allure.step(f"Регистрируем пользователя без поля '{missing_field}'"):
            response = api_client.register_user(registration_payload)

        with allure.step("Проверяем статус 403 и сообщение об ошибке"):
            assert_error_response(response, 403, ApiErrorMessages.REQUIRED_FIELDS)
