from fastapi import HTTPException, status
from uuid import UUID
from app.repository.nofication_settings import NotificationSettingsRepository
from app.repository.sent_job import SentJobRepository
from app.models.notification_settings import NotificationSettings
from app.schemas.nofication import NotificationSettingsUpdate, NotificationSettingsResponse
from app.schemas.job import JobResponse

class NotificationService:
    def __init__(
        self,
        notification_settings_repo: NotificationSettingsRepository,
        sent_job_repo: SentJobRepository,
    ):
        self.notification_settings_repo = notification_settings_repo
        self.sent_job_repo = sent_job_repo

    async def get_settings(self, user_id: UUID) -> NotificationSettingsResponse:
        settings = await self.notification_settings_repo.get_by_user_id(user_id)

        if not settings:
            settings = await self.notification_settings_repo.create(
                NotificationSettings(user_id=user_id)
            )

        return NotificationSettingsResponse.model_validate(settings)

    async def update_settings(
        self, user_id: UUID, data: NotificationSettingsUpdate
    ) -> NotificationSettingsResponse:
        settings = await self.notification_settings_repo.get_by_user_id(user_id)

        if not settings:
            settings = await self.notification_settings_repo.create(
                NotificationSettings(user_id=user_id) 
            )

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(settings, field, value)

        updated = await self.notification_settings_repo.update(settings)
        return NotificationSettingsResponse.model_validate(updated)  

    async def get_history(
        self, user_id: UUID, skip: int = 0, limit: int = 10
    ) -> list[JobResponse]:
        sent_jobs = await self.sent_job_repo.get_history(user_id, skip, limit)
        return [JobResponse.model_validate(sj.job) for sj in sent_jobs]