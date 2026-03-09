from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from backend.models.user import UserCreate, UserLogin, UserResponse, Token
from backend.services.auth_service import auth_service
from jose import JWTError, jwt
from backend.core.config import settings

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login/form")

async def get_current_user_dep(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    user = await auth_service.get_current_user(user_id)
    if user is None:
        raise credentials_exception
    return user

@router.post("/register", response_model=UserResponse)
async def register(user_in: UserCreate):
    """Register a new user."""
    created_user = await auth_service.register_user(user_in)
    return UserResponse.from_mongo(created_user)

@router.post("/login", response_model=Token)
async def login(user_in: UserLogin):
    """Login a user from JSON payload, returning access token."""
    return await auth_service.authenticate_user(user_in)

@router.post("/login/form", response_model=Token)
async def login_form(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login a user from Form data (Swagger UI support), returning access token."""
    return await auth_service.authenticate_user(UserLogin(email=form_data.username, password=form_data.password))

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: dict = Depends(get_current_user_dep)):
    """Get the currently logged in user info."""
    return UserResponse.from_mongo(current_user)
