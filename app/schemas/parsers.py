from pydantic import BaseModel
from app.models.enums.job_enum import JobRemote, JobLevel, JobSource

class RunParserRequest(BaseModel):
    source: JobSource
    technologies: list[str]
    level: JobLevel | None = None
    remote_type: JobRemote | None = None