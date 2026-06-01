import requests
import allure

from data import Urls, Messages


@allure.feature("Логин пользователя")
class TestLoginUser:

    @allure.title("Вход под существующим пользователем возвращает 200 и accessToken")
    def test_login_existing_user(self, created_user):
        user_data, _ = created_user
        payload = {"email": user_data["email"], "password": user_data["password"]}

        with allure.step("Логинимся существующим пользователем"):
            response = requests.post(Urls.LOGIN, json=payload)
        body = response.json()

        with allure.step("Проверяем статус 200 и тело ответа"):
            assert response.status_code == 200
            assert body["success"] is True
            assert body.get("accessToken")

    @allure.title("Вход с неверным логином и паролем возвращает 401")
    def test_login_with_wrong_credentials(self):
        payload = {"email": "no-such-user@yandex.ru", "password": "wrong-password"}

        with allure.step("Логинимся с несуществующими данными"):
            response = requests.post(Urls.LOGIN, json=payload)
        body = response.json()

        with allure.step("Проверяем статус 401 и сообщение об ошибке"):
            assert response.status_code == 401
            assert body["success"] is False
            assert body["message"] == Messages.INCORRECT_CREDENTIALS
