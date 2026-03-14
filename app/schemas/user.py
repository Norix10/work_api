from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class UserCreate(BaseModel):
    telegram_id: int
    username: str | None = None

class UserUpdate(BaseModel):
    username: str | None = None 

class UserResponse(BaseModel):
    id: UUID
    telegram_id: int
    username: str | None
    role: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True} 