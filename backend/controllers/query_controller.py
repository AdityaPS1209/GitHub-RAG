from fastapi import APIRouter, Depends, HTTPException, status
from backend.models.query import QueryRequest, QueryResponse, QueryHistoryModel
from backend.services.query_service import query_service
from backend.controllers.auth_controller import get_current_user_dep
from backend.core.database import get_database

router = APIRouter()

@router.post("/", response_model=QueryResponse)
async def execute_query(
    request: QueryRequest,
    current_user: dict = Depends(get_current_user_dep)
):
    try:
        response_data = await query_service.process_query(
            query=request.query,
            user_id=str(current_user["_id"]),
            repo_id=request.repo_id
        )
        return QueryResponse(**response_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while processing the query: {str(e)}"
        )

@router.get("/history")
async def get_query_history(
    limit: int = 50,
    current_user: dict = Depends(get_current_user_dep)
):
    db = get_database()
    cursor = db.query_history.find({"user_id": str(current_user["_id"])}).sort("created_at", -1).limit(limit)
    history = await cursor.to_list(length=limit)
    
    # Format ObjectIds
    for doc in history:
        doc["id"] = str(doc["_id"])
        del doc["_id"]
        
    return history
