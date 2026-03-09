from pydantic_settings import BaseSettings
from pydantic import Field
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "RAG Assistant API"
    API_V1_STR: str = "/api/v1"
    
    # MongoDB Settings
    MONGODB_URL: str = Field(default="mongodb://localhost:27017")
    MONGODB_DB_NAME: str = Field(default="rag_assistant")
    
    # Redis Settings
    REDIS_URL: str = Field(default="redis://localhost:6379/0")
    
    # JWT Settings
    SECRET_KEY: str = Field(default="your-super-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # 7 days
    
    # Groq / LLM Settings
    GROQ_API_KEY: str = Field(default="")
    
    class Config:
        environment_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
        env_file = environment_path
        case_sensitive = True

settings = Settings()
