from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from models.enums.job_enum import JobRemote, JobLevel, JobSource

class JobCreate(BaseModel):
    title: str
    company: str | None = None        
    url: str
    description: str | None = None   
    salary_min: int | None = None
    salary_max: int | None = None
    level: JobLevel | None = None    
    technologies: list[str] | None = None
    remote_type: JobRemote | None = None
    source: JobSource

class JobResponse(BaseModel):
    id: UUID
    title: str
    company: str | None
    url: str
    description: str | None
    salary_min: int | None
    salary_max: int | None
    level: JobLevel | None
    technologies: list[str] | None
    remote_type: JobRemote | None
    source: JobSource
    created_at: datetime

    model_config = {"from_attributes": True} 

class JobSearchRequest(BaseModel):
    technologies: list[str] | None = None
    level: JobLevel | None = None
    salary_min: int | None = None
    remote_type: JobRemote | None = None

class JobListResponse(BaseModel):
    items: list[JobResponse]
    total: int
    page: int
    limit: int

    model_config = {"from_attributes": True} 