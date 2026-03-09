from fastapi import HTTPException, status
from backend.models.user import UserCreate, UserLogin, UserModel
from backend.repositories.user_repo import user_repository
from backend.core.security import get_password_hash, verify_password, create_access_token
from backend.core.config import settings
from datetime import timedelta

class AuthService:
    async def register_user(self, user_in: UserCreate) -> dict:
        # Check if user exists
        user = await user_repository.get_user_by_email(user_in.email)
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this email already exists."
            )
            
        # Hash password and create user
        user_dict = user_in.model_dump()
        user_dict["hashed_password"] = get_password_hash(user_dict.pop("password"))
        
        # Pydantic model validates and provides structure/defaults
        new_user = UserModel(**user_dict)
        
        # Persist to DB
        created_user = await user_repository.create_user(new_user.model_dump(by_alias=True, exclude={"id"}))
        return created_user

    async def authenticate_user(self, user_in: UserLogin) -> dict:
        user = await user_repository.get_user_by_email(user_in.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if not verify_password(user_in.password, user["hashed_password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Create token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user["_id"]), "email": user["email"]},
            expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}

    async def get_current_user(self, user_id: str) -> dict:
        user = await user_repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

auth_service = AuthService()
