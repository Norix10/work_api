from pydantic import BaseModel 

class TelegramAuthRequest(BaseModel):
    telegram_id: int
    username: str | None = None

class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshTokenRequest(BaseModel):
    refresh_token: str