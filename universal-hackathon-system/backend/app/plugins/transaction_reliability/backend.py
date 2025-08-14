from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from statistics import mean
from ...db import get_db
from ...models import Event

router = APIRouter(tags=["plugin:transaction_reliability"])


@router.get("/reliability")
def reliability(db: Session = Depends(get_db)):
    events = db.query(Event).filter(Event.type == "transaction").all()
    amounts = [float(e.payload.get("amount", 0.0)) for e in events]
    avg_amount = mean(amounts) if amounts else 0.0
    return {"transactions": len(events), "avg_amount": round(avg_amount, 2)}