from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..db import get_db
from ..models import Notification, User
from ..schemas import NotificationCreate, NotificationOut
from .emailer import send_email
from ..auth.deps import get_current_user

router = APIRouter(prefix="/notify", tags=["notifications"])


@router.post("/email")
def notify_email(payload: NotificationCreate, db: Session = Depends(get_db)):
    user = None
    if payload.user_id:
        user = db.get(User, payload.user_id)
    to_email = user.email if user else "demo@example.com"
    try:
        send_email(to_email, payload.title, payload.message)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"status": "queued"}


@router.post("/inapp", response_model=NotificationOut)
def notify_inapp(payload: NotificationCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    target_user_id = payload.user_id or current_user.id
    notif = Notification(user_id=target_user_id, title=payload.title, message=payload.message)
    db.add(notif)
    db.commit()
    db.refresh(notif)
    return notif


@router.get("/inapp", response_model=List[NotificationOut])
def list_inapp(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    rows = db.query(Notification).filter(Notification.user_id == current_user.id).order_by(Notification.created_at.desc()).all()
    return rows