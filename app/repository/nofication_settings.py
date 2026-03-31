from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from app.repository.base import BaseRepository
from app.models.notification_settings import NotificationSettings

class NotificationSettingsRepository(BaseRepository[NotificationSettings]):
    def __init__(self, session: AsyncSession):
        super().__init__(NotificationSettings, session)

    async def get_by_user_id(self, user_id: UUID) -> NotificationSettings | None:
        result = await self.session.execute(
            select(NotificationSettings).where(NotificationSettings.user_id == user_id)
        )
        return result.scalar_one_or_none()