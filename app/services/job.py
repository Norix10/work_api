from fastapi import HTTPException, status
from uuid import UUID

from app.models.job import Job
from app.repository.filter import FilterRepository
from app.repository.job import JobRepository
from app.schemas.job import JobCreate, JobResponse, JobSearchRequest, JobListResponse

class JobService:
    def __init__(self, job_repo: JobRepository, filter_repo: FilterRepository):
        self.job_repo = job_repo
        self.filter_repo = filter_repo
    
    async def get_jobs(self, skip: int = 0, limit: int = 100) -> JobListResponse:
        jobs = await self.job_repo.get_all(skip=skip, limit=limit)
        return JobListResponse(
            items=[JobResponse.model_validate(j) for j in jobs],
            total=len(jobs),
            page=skip // limit + 1,
            limit=limit
        )

    async def get_job(self, job_id: UUID) -> JobResponse:
        job = await self.job_repo.get_by_id(job_id)
        if not job:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
        return JobResponse.model_validate(job)


    async def get_matched_jobs(self, user_id: UUID) -> list[JobResponse]:
        filters = await self.filter_repo.get_active_by_user_id(user_id)
        if not filters:
            raise HTTPException(404, "No active filters found")
        all_jobs = []
        seen_ids = set()
        for f in filters:
            search_job = JobSearchRequest(
                technologies=[t.lower() for t in f.technologies],
                level=f.level,
                salary_min=f.salary_min,
                remote_type=f.remote_type
            )
            jobs = await self.job_repo.get_matched_jobs(search_job)
            for job in jobs:
                if job.id not in seen_ids:
                    seen_ids.add(job.id)
                    all_jobs.append(JobResponse.model_validate(job))
        return all_jobs

    async def search_jobs(self, data: JobSearchRequest) -> list[JobResponse]:
        jobs = await self.job_repo.get_matched_jobs(data)
        return [JobResponse.model_validate(j) for j in jobs]

    async def save_jobs(self, jobs: list[JobCreate], technologies: list[str]) -> int:
        saved = 0
        for job in jobs:
            exists = await self.job_repo.exists_by_url(job.url)
            if not exists:

                job_obj = Job(**job.model_dump())
                job_obj.technologies = [t.lower() for t in technologies]
                await self.job_repo.create(job_obj)
                saved += 1
        return saved