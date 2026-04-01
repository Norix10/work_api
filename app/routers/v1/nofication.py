from fastapi import APIRouter, Depends, status
from uuid import UUID

from app.core.dependencies import get_notification_service, get_current_user
from app.schemas.nofication import NotificationSettingsUpdate, NotificationSettingsResponse
from app.models.user import User
from app.services.nofication import NotificationService

router = APIRouter(prefix="/notifications", tags=["notifications"])

@router.get("/settings", response_model=NotificationSettingsResponse)
async def get_notification_settings(
    current_user: User = Depends(get_current_user),
    service: NotificationService = Depends(get_notification_service)
) -> NotificationSettingsResponse:
    return await service.get_settings(current_user.id)

@router.put("/settings", response_model=NotificationSettingsResponse)
async def update_notification_settings(
    data: NotificationSettingsUpdate,
    current_user: User = Depends(get_current_user),
    service: NotificationService = Depends(get_notification_service)
) -> NotificationSettingsResponse:
    return await service.update_settings(current_user.id, data)

@router.get("/history", response_model=list[NotificationSettingsResponse]) 
async def get_notification_history(
    skip: int = 0,
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    service: NotificationService = Depends(get_notification_service)
) -> list[NotificationSettingsResponse]:
    return await service.get_history(current_user.id, skip, limit)
