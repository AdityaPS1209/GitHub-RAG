from celery import Celery
from backend.core.config import settings

# Since we don't have a reliable windows redis yet, we'll try to just hook it up and let user run solo pool later
celery_app = Celery(
    "rag_assistant_worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["backend.workers.tasks"]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_always_eager=True, # Run tasks synchronously, bypassing Redis broker if it's down

)
