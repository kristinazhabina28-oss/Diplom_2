import requests
import allure

from data import Urls, Messages


@allure.feature("Создание заказа")
class TestCreateOrder:

    @allure.title("Заказ с авторизацией и ингредиентами возвращает 200 и номер заказа")
    def test_create_order_authorized_with_ingredients(self, created_user, ingredients):
        _, access_token = created_user
        payload = {"ingredients": ingredients[:2]}

        with allure.step("Создаём заказ с токеном авторизации"):
            response = requests.post(
                Urls.ORDERS, json=payload, headers={"Authorization": access_token}
            )
        body = response.json()

        with allure.step("Проверяем статус 200, success и номер заказа"):
            assert response.status_code == 200
            assert body["success"] is True
            assert body["order"]["number"] > 0

    @allure.title("Заказ без авторизации возвращает 401 (по документации)")
    def test_create_order_without_auth(self, ingredients):
        payload = {"ingredients": ingredients[:2]}

        with allure.step("Создаём заказ без токена авторизации"):
            response = requests.post(Urls.ORDERS, json=payload)
        body = response.json()

        with allure.step("Проверяем статус 401 и сообщение об ошибке"):
            assert response.status_code == 401
            assert body["success"] is False
            assert body["message"] == Messages.NOT_AUTHORISED

    @allure.title("Заказ с валидными ингредиентами возвращает 200 и номер заказа")
    def test_create_order_with_ingredients(self, created_user, ingredients):
        _, access_token = created_user
        payload = {"ingredients": ingredients[:3]}

        with allure.step("Создаём заказ с валидными хешами ингредиентов"):
            response = requests.post(
                Urls.ORDERS, json=payload, headers={"Authorization": access_token}
            )
        body = response.json()

        with allure.step("Проверяем статус 200, success и номер заказа"):
            assert response.status_code == 200
            assert body["success"] is True
            assert body["order"]["number"] > 0

    @allure.title("Заказ без ингредиентов возвращает 400")
    def test_create_order_without_ingredients(self, created_user):
        _, access_token = created_user
        payload = {"ingredients": []}

        with allure.step("Создаём заказ с пустым списком ингредиентов"):
            response = requests.post(
                Urls.ORDERS, json=payload, headers={"Authorization": access_token}
            )
        body = response.json()

        with allure.step("Проверяем статус 400 и сообщение об ошибке"):
            assert response.status_code == 400
            assert body["success"] is False
            assert body["message"] == Messages.INGREDIENTS_REQUIRED

    @allure.title("Заказ с неверным хешем ингредиента возвращает 500")
    def test_create_order_with_invalid_ingredient_hash(self, created_user):
        _, access_token = created_user
        payload = {"ingredients": ["invalid_hash_123", "another_bad_hash"]}

        with allure.step("Создаём заказ с невалидными хешами ингредиентов"):
            response = requests.post(
                Urls.ORDERS, json=payload, headers={"Authorization": access_token}
            )

        with allure.step("Проверяем статус 500"):
            assert response.status_code == 500
