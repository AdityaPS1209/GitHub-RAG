from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.core.config import settings
from backend.core.database import connect_to_mongo, close_mongo_connection

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_db_client():
    connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_db_client():
    close_mongo_connection()

from backend.controllers import auth_controller, ingest_controller, query_controller

@app.get("/")
def root():
    return {"message": "Welcome to the RAG Assistant API"}

app.include_router(auth_controller.router, prefix=f"{settings.API_V1_STR}/auth", tags=["Auth"])
app.include_router(ingest_controller.router, prefix=f"{settings.API_V1_STR}/ingest", tags=["Ingestion"])
app.include_router(query_controller.router, prefix=f"{settings.API_V1_STR}/query", tags=["Query"])
