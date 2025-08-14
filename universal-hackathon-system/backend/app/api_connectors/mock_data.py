from faker import Faker
from random import random, choice
from datetime import datetime

fake = Faker()


def generate_mock_event() -> dict:
    return {
        "type": choice(["transaction", "signup", "error", "metric"]),
        "payload": {
            "user": fake.email(),
            "amount": round(random() * 1000, 2),
            "timestamp": datetime.utcnow().isoformat(),
            "message": fake.sentence(),
        },
    }