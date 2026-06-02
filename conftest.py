import pytest

from api_client import StellarBurgersApi
from helpers import build_unique_user_payload


@pytest.fixture
def api_client():
    return StellarBurgersApi()


@pytest.fixture
def new_user_payload():
    return build_unique_user_payload()


@pytest.fixture
def registered_user(api_client, new_user_payload):
    response = api_client.register_user(new_user_payload)
    response_body = response.json()
    user_access_token = response_body.get("accessToken")

    yield new_user_payload, user_access_token

    if user_access_token:
        api_client.delete_user(user_access_token)


@pytest.fixture
def ingredient_ids(api_client):
    response = api_client.get_ingredients()
    response_body = response.json()["data"]
    return [item["_id"] for item in response_body]
