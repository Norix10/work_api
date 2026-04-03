from fastapi import APIRouter, Depends, status

from app.core.dependencies import get_user_service, get_current_user
from app.schemas.user import UserResponse, UserUpdate
from app.models.user import User
from app.services.user import UserService

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserResponse)
async def get_me(
    current_user: User = Depends(get_current_user),
    service: UserService = Depends(get_user_service)
) -> UserResponse:
    return await service.get_me(current_user.id)

@router.post("/me/deactivate", status_code=status.HTTP_204_NO_CONTENT)
async def deactivate_me(
    current_user: User = Depends(get_current_user),
    service: UserService = Depends(get_user_service)
) -> None:
    await service.deactivate_me(current_user.id)

@router.put("/me", response_model=UserResponse)
async def update_me(
    data: UserUpdate,
    current_user: User = Depends(get_current_user),
    service: UserService = Depends(get_user_service)
) -> UserResponse:
    return await service.update_me(current_user.id, data)

@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_me(
    current_user: User = Depends(get_current_user),
    service: UserService = Depends(get_user_service)
) -> None:
    await service.delete_me(current_user.id)

