from fastapi import APIRouter, Depends, status

from app.core.dependencies import get_auth_service
from app.services.auth import AuthService
from app.schemas.auth import TelegramAuthRequest, RefreshTokenRequest, AuthResponse

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/telegram", response_model=AuthResponse)
async def authenticate_with_telegram(
    data: TelegramAuthRequest,
    service: AuthService = Depends(get_auth_service)
) -> AuthResponse:
    return await service.telegram_auth(data)


@router.post("/refresh", response_model=AuthResponse)
async def refresh_token(
    data: RefreshTokenRequest,
    service: AuthService = Depends(get_auth_service)
) -> AuthResponse:
    return await service.refresh_token(data.refresh_token)

@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    data: RefreshTokenRequest,
    service: AuthService = Depends(get_auth_service)
) -> None:
    await service.logout(data.refresh_token)
