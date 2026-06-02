import requests

from data import ApiRoutes


DEFAULT_TIMEOUT = 10


class StellarBurgersApi:
    def __init__(self, timeout=DEFAULT_TIMEOUT):
        self.timeout = timeout

    def register_user(self, user_payload):
        return requests.post(
            ApiRoutes.REGISTER, json=user_payload, timeout=self.timeout
        )

    def login_user(self, credentials):
        return requests.post(ApiRoutes.LOGIN, json=credentials, timeout=self.timeout)

    def delete_user(self, access_token):
        return requests.delete(
            ApiRoutes.USER,
            headers={"Authorization": access_token},
            timeout=self.timeout,
        )

    def get_ingredients(self):
        return requests.get(ApiRoutes.INGREDIENTS, timeout=self.timeout)

    def create_order(self, order_payload, access_token=None):
        headers = {"Authorization": access_token} if access_token else None
        return requests.post(
            ApiRoutes.ORDERS,
            json=order_payload,
            headers=headers,
            timeout=self.timeout,
        )
