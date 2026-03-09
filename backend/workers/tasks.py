import asyncio
from backend.workers.celery_app import celery_app
from backend.services.ingestion_service import ingestion_service

@celery_app.task(name="ingest_github_repo_task")
def ingest_github_repo_task(repo_id: str, clone_url: str):
    # Celery tasks are synchronous, but our service uses async motor calls.
    # We must run the async function in an event loop.
    asyncio.run(ingestion_service.ingest_repository(repo_id, clone_url))
    return {"status": "completed", "repo_id": repo_id}
