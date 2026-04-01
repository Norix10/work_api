from fastapi import APIRouter, Depends, status
from uuid import UUID

from app.core.dependencies import get_job_service, get_current_user
from app.schemas.job import JobResponse, JobSearchRequest
from app.models.user import User
from app.services.job import JobService

router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.get("/", response_model=list[JobResponse])
async def get_jobs(
    skip: int = 0,
    limit: int = 100,
    service: JobService = Depends(get_job_service)
) -> list[JobResponse]:
    return await service.get_jobs(skip, limit)

@router.get("/matched", response_model=list[JobResponse])
async def get_matched_jobs(
    current_user: User = Depends(get_current_user),
    service: JobService = Depends(get_job_service)
) -> list[JobResponse]:
    return await service.get_matched_jobs(current_user.id)

@router.get("/{job_id}", response_model=JobResponse)
async def get_job(
    job_id: UUID,
    service: JobService = Depends(get_job_service)
) -> JobResponse:
    return await service.get_job(job_id)

@router.post("/search", response_model=list[JobResponse])
async def search_jobs(
    data: JobSearchRequest,
    service: JobService = Depends(get_job_service)
) -> list[JobResponse]:
    return await service.search_jobs(data)

