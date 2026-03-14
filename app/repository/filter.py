# get_by_user_id(user_id)
# get_active_by_user_id(user_id)

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from uuid import UUID

from app.repository.base import BaseRepository
from app.models.filter import Filter


class FilterRepository(BaseRepository[Filter]):
    def __init__(self, session: AsyncSession):
        super().__init__(Filter, session)

    async def get_by_user_id(self, user_id: UUID) -> list[Filter]:
        result = await self.session.execute(
            select(Filter).where(Filter.user_id == user_id)
        )
        return result.scalars().all()

    async def get_active_by_user_id(self, user_id: UUID) -> list[Filter]:
        result = await self.session.execute(
            select(Filter).where(Filter.user_id == user_id, Filter.is_active == True)
        )
        return list(result.scalars().all())
