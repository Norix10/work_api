from app.models.enums.job_enum import JobSource
from pydantic import BaseModel

class RunParserRequest(BaseModel):
    source: JobSource  