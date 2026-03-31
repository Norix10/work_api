from fastapi import HTTPException, status
from uuid import UUID

from app.models.filter import Filter
from app.models.user import User
from app.repository.filter import FilterRepository
from app.schemas.filter import FilterResponse, FilterCreate, FilterUpdate


class FilterService:
    def __init__(self, filter_repo: FilterRepository):
        self.filter_repo = filter_repo

    async def get_filters(self, user_id: UUID) -> list[FilterResponse]:
        filters = await self.filter_repo.get_by_user_id(user_id)
        if not filters:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Filter not found"
            )
        return [FilterResponse.model_validate(f) for f in filters]

    async def create_filters(self, user_id: UUID, data: FilterCreate) -> FilterResponse:
        filter_obj = await self.filter_repo.create(
            Filter(user_id=user_id, **data.model_dump())
        )
        return FilterResponse.model_validate(filter_obj)

    async def update_filters(self, filter_id: UUID, user_id: UUID, data: FilterUpdate) -> FilterResponse:
        filter_obj = await self.filter_repo.get_by_id(filter_id)
        if not filter_obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
        if filter_obj.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(filter_obj, field, value)

        updated_user = await self.filter_repo.update(filter_obj)
        return FilterResponse.model_validate(updated_user)

    async def delete_filter(self, user_id: UUID, filter_id: UUID) -> None:
        filter = await self.filter_repo.get_by_id(filter_id)
        if not filter:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Not found"
            )
        if filter.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden"
            )
        await self.filter_repo.delete(filter)

    async def delete_all_filters(self, user_id: UUID) -> None:
        filters = await self.filter_repo.get_by_id(user_id)
        for f in filters:
            await self.filter_repo.delete(f)
