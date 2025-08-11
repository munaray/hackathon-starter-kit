from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import Event
from ..schemas import EventIn, EventOut
from ..events.redis_client import publish_event
from .mock_data import generate_mock_event

router = APIRouter(prefix="/ingest", tags=["ingestion"])


@router.post("/event", response_model=EventOut)
def ingest_event(payload: EventIn, db: Session = Depends(get_db)):
    event = Event(type=payload.type, payload=payload.payload)
    db.add(event)
    db.commit()
    db.refresh(event)
    publish_event({"id": event.id, "type": event.type, "payload": event.payload, "created_at": event.created_at.isoformat()})
    return event


@router.post("/mock", response_model=EventOut)
def ingest_mock(db: Session = Depends(get_db)):
    data = generate_mock_event()
    event = Event(type=data["type"], payload=data["payload"])
    db.add(event)
    db.commit()
    db.refresh(event)
    publish_event({"id": event.id, "type": event.type, "payload": event.payload, "created_at": event.created_at.isoformat()})
    return event