from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Any
from datetime import datetime

class PyObjectId(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, info=None): # Updated for Pydantic v2
        if not isinstance(v, str):
            raise ValueError("Invalid ObjectId")
        return v

    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type: Any, _handler: Any):
        from pydantic_core import core_schema
        return core_schema.str_schema()

class UserModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str = Field(...)
    email: EmailStr = Field(...)
    hashed_password: str = Field(...)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "name": "Jane Doe",
                "email": "jdoe@example.com",
                "hashed_password": "strongpassword"
            }
        }

class UserCreate(BaseModel):
    name: str = Field(..., min_length=2)
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

class UserResponse(BaseModel):
    val_id: str = Field(alias="id") # using val_id instead of id to prevent conflicts
    name: str
    email: EmailStr
    
    @staticmethod
    def from_mongo(mongo_doc: dict):
        return UserResponse(
            id=str(mongo_doc.get("_id")),
            name=mongo_doc.get("name"),
            email=mongo_doc.get("email")
        )

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    user_id: Optional[str] = None
