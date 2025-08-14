from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from .config import settings
from .db import Base, engine
from .utils.logger import logger

from .auth.router import router as auth_router
from .api_connectors.router import router as ingest_router
from .analytics.router import router as analytics_router
from .events.router import router as events_router
from .notifications.router import router as notify_router
from .plugins.loader import load_plugins, build_plugins_router

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy.orm import Session
from .db import SessionLocal
from .api_connectors.mock_data import generate_mock_event
from .models import Event
from .events.redis_client import publish_event


app = FastAPI(title="Universal Hackathon System", default_response_class=ORJSONResponse)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables on startup
Base.metadata.create_all(bind=engine)

# Routers
app.include_router(auth_router)
app.include_router(ingest_router)
app.include_router(analytics_router)
app.include_router(events_router)
app.include_router(notify_router)

# Plugins
plugins_meta = load_plugins(app)
app.include_router(build_plugins_router(plugins_meta))


scheduler = AsyncIOScheduler()


def scheduled_mock_ingest():
    logger.info("Running scheduled mock ingest")
    db: Session = SessionLocal()
    try:
        data = generate_mock_event()
        e = Event(type=data["type"], payload=data["payload"]) 
        db.add(e)
        db.commit()
        db.refresh(e)
        publish_event({"id": e.id, "type": e.type, "payload": e.payload, "created_at": e.created_at.isoformat()})
    finally:
        db.close()


@app.on_event("startup")
async def on_startup():
    if settings.scheduler_cron:
        scheduler.add_job(scheduled_mock_ingest, CronTrigger.from_crontab(settings.scheduler_cron))
    else:
        # default: every 60 seconds
        scheduler.add_job(scheduled_mock_ingest, "interval", seconds=60)
    scheduler.start()
    logger.info("Scheduler started")


@app.on_event("shutdown")
async def on_shutdown():
    scheduler.shutdown(wait=False)
    logger.info("Scheduler stopped")