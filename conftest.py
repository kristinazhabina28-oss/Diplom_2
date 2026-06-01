import requests
import pytest

from data import Urls
from helpers import generate_user


@pytest.fixture
def user_data():
    return generate_user()


@pytest.fixture
def created_user(user_data):
    response = requests.post(Urls.REGISTER, json=user_data)
    body = response.json()
    access_token = body.get("accessToken")

    yield user_data, access_token

    if access_token:
        requests.delete(Urls.USER, headers={"Authorization": access_token})


@pytest.fixture
def ingredients():
    response = requests.get(Urls.INGREDIENTS)
    data = response.json()["data"]
    return [item["_id"] for item in data]
