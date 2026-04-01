from fastapi import APIRouter, Depends, status
from uuid import UUID   

from app.core.dependencies import get_filter_service, get_current_user
from app.schemas.filter import FilterCreate, FilterUpdate, FilterResponse
from app.models.user import User
from app.services.filter import FilterService

router = APIRouter(prefix="/filters", tags=["filters"])

@router.get("/", response_model=list[FilterResponse])
async def get_filters(
    current_user: User = Depends(get_current_user),
    service: FilterService = Depends(get_filter_service)
) -> list[FilterResponse]:
    return await service.get_filters(current_user.id)

@router.post("/", response_model=FilterResponse)
async def create_filter(
    data: FilterCreate,
    current_user: User = Depends(get_current_user),
    service: FilterService = Depends(get_filter_service)
) -> FilterResponse:
    return await service.create_filter(current_user.id, data)

@router.put("/{filter_id}", response_model=FilterResponse)
async def update_filter(
    filter_id: UUID,
    data: FilterUpdate,
    current_user: User = Depends(get_current_user),
    service: FilterService = Depends(get_filter_service)
) -> FilterResponse:
    return await service.update_filter(current_user.id, filter_id, data)

@router.delete("/{filter_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_filter(
    filter_id: UUID,
    current_user: User = Depends(get_current_user),
    service: FilterService = Depends(get_filter_service)
) -> None:
    await service.delete_filter(current_user.id, filter_id)


