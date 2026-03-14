# is_already_sent(user_id, job_id)
# get_history(user_id, skip, limit)

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from uuid import UUID

from app.repository.base import BaseRepository
from app.models.sent_job import SentJob


class SentJobRepository(BaseRepository[SentJob]):
    def __init__(self, session: AsyncSession):
        super().__init__(SentJob, session)

    async def is_already_sent(self, user_id: UUID, job_id: UUID) -> bool: 
        result = await self.session.execute(
            select(SentJob).where(SentJob.user_id == user_id, SentJob.job_id == job_id)
        )
        return result.scalar_one_or_none() is not None
    
    async def get_history(self, user_id: UUID, skip: int = 0, limit = 100) -> list[SentJob]:
        result = await self.session.execute(
            select(SentJob).where(SentJob.user_id == user_id).offset(skip).limit(limit)
        )
        return list(result.scalars().all())

