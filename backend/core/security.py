from datetime import datetime, timedelta
from jose import jwt
import bcrypt
from backend.core.config import settings

def verify_password(plain_password, hashed_password):
    # Truncate to 72 chars to avoid bcrypt ValueError (> 72 bytes)
    pwd_bytes = plain_password.encode('utf-8')[:72]
    
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode('utf-8')
        
    try:
        return bcrypt.checkpw(pwd_bytes, hashed_password)
    except Exception:
        return False

def get_password_hash(password):
    # Truncate to 72 chars to avoid bcrypt ValueError (> 72 bytes)
    pwd_bytes = password.encode('utf-8')[:72]
    return bcrypt.hashpw(pwd_bytes, bcrypt.gensalt()).decode('utf-8')

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
        
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt
