import uuid


def generate_webhook_id() -> str:
    return str(uuid.uuid4())
