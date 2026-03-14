from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from app.repository.base import BaseRepository
from app.models.job import Job
from app.schemas.job import JobSearchRequest


class JobRepository(BaseRepository[Job]):
    def __init__(self, session: AsyncSession):
        super().__init__(Job, session)

    async def get_by_url(self, url: str) -> Job | None:
        result = await self.session.execute(select(Job).where(Job.url == url))
        return result.scalar_one_or_none()

    async def exists_by_url(self, url: str) -> bool:
        result = await self.session.execute(select(Job.id).where(Job.url == url))
        return result.scalar_one_or_none() is not None

    async def get_matched_jobs(self, filters: JobSearchRequest) -> list[Job]:  
        query = select(Job)

        if filters.technologies:
            query = query.where(Job.technologies.overlap(filters.technologies))
        if filters.level:
            query = query.where(Job.level == filters.level)
        if filters.salary_min:
            query = query.where(Job.salary_min >= filters.salary_min)  
        if filters.remote_type:
            query = query.where(Job.remote_type == filters.remote_type)

        result = await self.session.execute(query)
        return list(result.scalars().all())

