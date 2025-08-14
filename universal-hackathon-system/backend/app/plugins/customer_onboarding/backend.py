from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...db import get_db
from ...models import Event

router = APIRouter(tags=["plugin:customer_onboarding"])


@router.get("/status")
def onboarding_status(db: Session = Depends(get_db)):
    total = db.query(Event).count()
    kyc = db.query(Event).filter(Event.type == "signup").count()
    return {"total_events": total, "kyc_signups": kyc}