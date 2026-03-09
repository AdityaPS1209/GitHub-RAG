from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, BackgroundTasks
from backend.models.document import IngestRepoRequest, RepositoryModel
from backend.controllers.auth_controller import get_current_user_dep
from backend.core.database import get_database
from backend.services.ingestion_service import ingestion_service
from bson import ObjectId
import os
import shutil

router = APIRouter()

@router.post("/ingest_repo")
async def ingest_repository(
    request: IngestRepoRequest,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user_dep)
):
    db = get_database()
    
    # Create a new repository record
    new_repo = RepositoryModel(
        url=request.github_url,
        owner_id=str(current_user["_id"])
    )
    
    result = await db.repositories.insert_one(new_repo.model_dump(by_alias=True, exclude={"id"}))
    repo_id = str(result.inserted_id)
    
    # Trigger Native FastAPI Background Task (Bypasses Celery/Redis entirely)
    background_tasks.add_task(ingestion_service.ingest_repository, repo_id, request.github_url)
    
    return {"message": "Repository ingestion started.", "repo_id": repo_id}

@router.post("/upload_docs")
async def upload_documents(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user_dep)
):
    # This is a stub for the file upload endpoint
    # In a full production app, we would save the file, create a celery task, and process it
    # similar to the github repository ingestion.
    return {"message": f"File {file.filename} uploaded for processing (Stub)."}

@router.get("/repositories")
async def get_repositories(current_user: dict = Depends(get_current_user_dep)):
    db = get_database()
    cursor = db.repositories.find({"owner_id": str(current_user["_id"])})
    repos = await cursor.to_list(length=100)
    
    # Convert ObjectIds to strings for JSON serialization
    for repo in repos:
        repo["id"] = str(repo["_id"])
        del repo["_id"]
        
    return repos
