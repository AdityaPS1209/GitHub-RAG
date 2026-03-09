from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from backend.models.user import PyObjectId

class QueryRequest(BaseModel):
    query: str
    repo_id: Optional[str] = None # If None, search across all user's repos
    
class SourceDocument(BaseModel):
    file_path: str
    content: str
    distance: float

class QueryResponse(BaseModel):
    answer: str
    sources: List[SourceDocument]
    
class QueryHistoryModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    user_id: str
    query: str
    answer: str
    sources: List[Dict[str, Any]]
    repo_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
