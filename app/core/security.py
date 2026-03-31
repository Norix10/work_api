import jwt
from jwt import InvalidTokenError
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/telegram")

def decode_token(token: str) -> str:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return user_id
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")