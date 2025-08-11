import asyncio
import json
from datetime import datetime, timedelta
from typing import List
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import Event
from .redis_client import get_redis

router = APIRouter(tags=["events"])  # no prefix for ws simplicity


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    r = get_redis()
    pubsub = r.pubsub()
    pubsub.subscribe("events")

    try:
        async def reader():
            while True:
                message = pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
                if message and message.get("data"):
                    await websocket.send_text(message["data"])  # type: ignore
                await asyncio.sleep(0.01)

        await reader()
    except WebSocketDisconnect:
        pass
    finally:
        try:
            pubsub.close()
        except Exception:
            pass


@router.get("/events", response_model=List[dict])
def list_events(db: Session = Depends(get_db)):
    rows = db.query(Event).order_by(Event.created_at.desc()).limit(100).all()
    return [
        {"id": e.id, "type": e.type, "payload": e.payload, "created_at": e.created_at.isoformat()} for e in rows
    ]


@router.get("/events/stats", response_model=dict)
def events_stats(db: Session = Depends(get_db)):
    since = datetime.utcnow() - timedelta(hours=2)
    rows = db.query(Event).filter(Event.created_at >= since).all()
    buckets: dict[str, int] = {}
    for e in rows:
        minute = e.created_at.replace(second=0, microsecond=0).isoformat()
        buckets[minute] = buckets.get(minute, 0) + 1
    return {"by_minute": buckets}