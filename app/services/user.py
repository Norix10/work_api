from fastapi import HTTPException, status
from uuid import UUID

from app.core.config import settings
from app.schemas.user import UserResponse, UserCreate, UserUpdate
from app.repository.user import UserRepository
from app.models.user import User

class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def get_me(self, user_id: UUID) -> UserResponse:
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return UserResponse.model_validate(user) 
    
    async def get_all_users(self, skip: int = 0, limit: int = 100) -> list[UserResponse]:
        users = await self.user_repo.get_all(skip=skip, limit=limit)
        return [UserResponse.model_validate(u) for u in users]

    async def update_me(self, user_id: UUID, user_data: UserUpdate) -> UserResponse:
        user = await self.user_repo.get_by_id(user_id) 
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        for field, value in user_data.model_dump(exclude_unset=True).items():
            setattr(user, field, value)

        updated_user = await self.user_repo.update(user)
        return UserResponse.model_validate(updated_user)

    async def deactivate_me(self, user_id: UUID) -> None:
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user.is_active = False
        await self.user_repo.update(user)

    async def delete_me(self, user_id: UUID) -> None:
        user = await self.user_repo.get_by_id(user_id)  
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        await self.user_repo.delete(user)  