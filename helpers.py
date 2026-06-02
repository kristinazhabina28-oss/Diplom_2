import uuid


def build_unique_user_payload():
    unique_suffix = uuid.uuid4().hex[:10]
    return {
        "email": f"stellar-{unique_suffix}@yandex.ru",
        "password": f"pass-{unique_suffix}",
        "name": f"user-{unique_suffix}",
    }
