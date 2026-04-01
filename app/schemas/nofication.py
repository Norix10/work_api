from pydantic import BaseModel, Field
from datetime import datetime

class NotificationSettingsUpdate(BaseModel):
    interval_hours: int | None = Field(None, ge=1, le=24) 
    is_active: bool | None = None

class NotificationSettingsResponse(BaseModel):
    interval_hours: int
    is_active: bool
    last_sent_at: datetime | None = None

    model_config = {"from_attributes": True}