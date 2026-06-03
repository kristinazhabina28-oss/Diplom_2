import allure

from assertions import Assertions
from data import ApiErrorMessages


@allure.feature("Логин пользователя")
class TestLoginUser:

    @allure.title("Вход под существующим пользователем возвращает 200 и accessToken")
    def test_login_existing_user(self, api_client, registered_user):
        registered_user_payload, _ = registered_user
        credentials = {
            "email": registered_user_payload["email"],
            "password": registered_user_payload["password"],
        }

        with allure.step("Логинимся существующим пользователем"):
            response = api_client.login_user(credentials)

        with allure.step("Проверяем статус 200 и тело ответа"):
            Assertions.assert_access_token_received(response)

    @allure.title("Вход с неверным логином и паролем возвращает 401")
    def test_login_with_wrong_credentials(self, api_client):
        wrong_credentials = {
            "email": "no-such-user@yandex.ru",
            "password": "wrong-password",
        }

        with allure.step("Логинимся с несуществующими данными"):
            response = api_client.login_user(wrong_credentials)

        with allure.step("Проверяем статус 401 и сообщение об ошибке"):
            Assertions.assert_error_response(
                response, 401, ApiErrorMessages.INCORRECT_CREDENTIALS
            )
