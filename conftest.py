import pytest

from api_client import StellarBurgersApi
from helpers import build_unique_user_payload


@pytest.fixture
def api_client():
    return StellarBurgersApi()


@pytest.fixture
def user_registrar(api_client):
    access_tokens = []

    def register_user(user_payload):
        response = api_client.register_user(user_payload)
        response_body = response.json()
        access_token = response_body.get("accessToken")
        if access_token:
            access_tokens.append(access_token)
        return response

    yield register_user

    for access_token in access_tokens:
        api_client.delete_user(access_token)


@pytest.fixture
def registered_user(user_registrar):
    user_payload = build_unique_user_payload()
    response = user_registrar(user_payload)
    response_body = response.json()

    yield user_payload, response_body.get("accessToken")
