import allure
import pytest

from assertions import Assertions
from data import ApiErrorMessages


@allure.feature("Создание заказа")
class TestCreateOrder:

    @allure.title("Заказ с авторизацией и ингредиентами возвращает 200 и номер заказа")
    def test_create_order_authorized_with_ingredients(
        self, api_client, registered_user
    ):
        _, user_access_token = registered_user
        ingredient_ids = api_client.get_ingredient_ids()
        order_payload = {"ingredients": ingredient_ids[:2]}

        with allure.step("Создаём заказ с токеном авторизации"):
            response = api_client.create_order(order_payload, user_access_token)

        with allure.step("Проверяем статус 200, success и номер заказа"):
            Assertions.assert_order_number_received(response)

    @allure.title("Заказ без авторизации возвращает 401 (по документации)")
    @pytest.mark.xfail(
        reason="API returns 200 for POST /api/orders without auth instead of documented 401",
        raises=AssertionError,
        strict=True,
    )
    def test_create_order_without_auth(self, api_client):
        ingredient_ids = api_client.get_ingredient_ids()
        order_payload = {"ingredients": ingredient_ids[:2]}

        with allure.step("Создаём заказ без токена авторизации"):
            response = api_client.create_order(order_payload)

        with allure.step("Проверяем статус 401 и сообщение об ошибке"):
            Assertions.assert_error_response(
                response, 401, ApiErrorMessages.NOT_AUTHORISED
            )

    @allure.title("Заказ с валидными ингредиентами возвращает 200 и номер заказа")
    def test_create_order_with_ingredients(
        self, api_client, registered_user
    ):
        _, user_access_token = registered_user
        ingredient_ids = api_client.get_ingredient_ids()
        order_payload = {"ingredients": ingredient_ids[:3]}

        with allure.step("Создаём заказ с валидными хешами ингредиентов"):
            response = api_client.create_order(order_payload, user_access_token)

        with allure.step("Проверяем статус 200, success и номер заказа"):
            Assertions.assert_order_number_received(response)

    @allure.title("Заказ без ингредиентов возвращает 400")
    def test_create_order_without_ingredients(self, api_client, registered_user):
        _, user_access_token = registered_user
        order_payload = {"ingredients": []}

        with allure.step("Создаём заказ с пустым списком ингредиентов"):
            response = api_client.create_order(order_payload, user_access_token)

        with allure.step("Проверяем статус 400 и сообщение об ошибке"):
            Assertions.assert_error_response(
                response, 400, ApiErrorMessages.INGREDIENTS_REQUIRED
            )

    @allure.title("Заказ с неверным хешем ингредиента возвращает 500")
    def test_create_order_with_invalid_ingredient_hash(self, api_client, registered_user):
        _, user_access_token = registered_user
        order_payload = {"ingredients": ["invalid_hash_123", "another_bad_hash"]}

        with allure.step("Создаём заказ с невалидными хешами ингредиентов"):
            response = api_client.create_order(order_payload, user_access_token)

        with allure.step("Проверяем статус 500"):
            Assertions.assert_status_code(response, 500)
