from sqlalchemy.orm import Session
from ..db import Base, engine, SessionLocal
from ..models import User, Event
from ..auth.utils import hash_password
from ..api_connectors.mock_data import generate_mock_event


def reset_and_seed():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    try:
        admin = User(email="admin@example.com", hashed_password=hash_password("admin"), role="admin")
        user = User(email="user@example.com", hashed_password=hash_password("user"), role="user")
        db.add_all([admin, user])
        for _ in range(10):
            data = generate_mock_event()
            e = Event(type=data["type"], payload=data["payload"])
            db.add(e)
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    reset_and_seed()