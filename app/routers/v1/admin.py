from fastapi import APIRouter, Depends, status, Query
from datetime import datetime, timedelta, timezone

from app.core.dependencies import get_current_admin, get_user_service, get_job_service
from app.models.user import User
from app.services.user import UserService
from app.services.job import JobService
from app.schemas.user import UserResponse
from app.schemas.parsers import RunParserRequest

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/users", response_model=list[UserResponse]) 
async def get_all_users(
    current_admin: User = Depends(get_current_admin),
    service: UserService = Depends(get_user_service),
) -> list[UserResponse]:
    return await service.get_all_users()


@router.post("/parsers/run", status_code=status.HTTP_200_OK)
async def run_parsers(
    data: RunParserRequest,
    current_admin: User = Depends(get_current_admin),
) -> dict[str, str]:
    return {"status": "started", "source": data.source}


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
