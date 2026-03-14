from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from app.models.enums.job_enum import JobLevel, JobRemote

class FilterCreate(BaseModel):
    technologies: list[str]
    level: JobLevel               
    salary_min: int
    remote_type: JobRemote

class FilterUpdate(BaseModel):
    technologies: list[str] | None = None
    level: JobLevel | None = None    
    salary_min: int | None = None
    remote_type: JobRemote | None = None

class FilterResponse(BaseModel):
    id: UUID
    user_id: UUID
    technologies: list[str]
    level: JobLevel
    salary_min: int | None
    remote_type: JobRemote
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}