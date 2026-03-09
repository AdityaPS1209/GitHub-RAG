from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from backend.models.user import PyObjectId

class RepositoryModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    url: str
    owner_id: str
    status: str = "pending" # pending, processing, completed, failed
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True

class DocumentChunk(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    repo_id: str
    file_path: str
    content: str
    chunk_index: int
    vector_id: Optional[int] = None # ID in FAISS
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True

class IngestRepoRequest(BaseModel):
    github_url: str
