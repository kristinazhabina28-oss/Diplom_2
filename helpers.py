import uuid


def generate_user():
    suffix = uuid.uuid4().hex[:10]
    return {
        "email": f"stellar-{suffix}@yandex.ru",
        "password": f"pass-{suffix}",
        "name": f"user-{suffix}",
    }
