from app.routers.v1 import health, user

from fastapi import APIRouter

api_router = APIRouter(prefix="/api/v1")

# api_router.include_router(booking.router)
api_router.include_router(health.router)

api_router.include_router(user.router)
# api_router.include_router()
