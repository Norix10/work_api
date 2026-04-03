from fastapi import APIRouter, Depends, status, Query
from datetime import datetime, timedelta, timezone

from app.core.dependencies import get_current_admin, get_user_service, get_job_service
from app.models.user import User
from app.services.user import UserService
from app.services.job import JobService
from app.schemas.user import UserResponse
from app.schemas.parsers import RunParserRequest
from parsers.djinni import DjinniParser
from parsers.djinni import DjinniParser
from app.models.enums.job_enum import JobSource
from parsers.dou import DouParser 

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/users", response_model=list[UserResponse]) 
async def get_all_users(
    current_admin: User = Depends(get_current_admin),
    service: UserService = Depends(get_user_service),
) -> list[UserResponse]:
    return await service.get_all_users()


@router.post("/parsers/run")
async def run_parsers(
    data: RunParserRequest,
    current_admin: User = Depends(get_current_admin),
    service: JobService = Depends(get_job_service)
) -> dict:
    if data.source == JobSource.djinni:
        parser = DjinniParser()
    if data.source == JobSource.dou:
        parser = DouParser()
    else:
        return {"status": "error", "detail": "Parser not implemented yet"}

    jobs = await parser.fetch_jobs(
        technologies=data.technologies,
        level=data.level.value if data.level else None,
        remote_type=data.remote_type.value if data.remote_type else None,
    )
    saved = await service.save_jobs(jobs, data.technologies)
    return {"status": "done", "source": data.source, "found": len(jobs), "saved": saved}


@router.get("/parsers/status")
async def get_parsers_status(
    current_admin: User = Depends(get_current_admin),
) -> dict[str, str]:
    return {"status": "running"}


@router.delete("/jobs/cleanup", status_code=status.HTTP_204_NO_CONTENT)
async def cleanup_old_jobs(
    older_than_days: int = Query(default=30, ge=1),
    job_service: JobService = Depends(get_job_service),
    current_admin: User = Depends(get_current_admin),
) -> None:
    pass
