from app.routers.v1 import admin, auth, filter, health, nofication, user, job

from fastapi import APIRouter

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(admin.router)
api_router.include_router(auth.router)
api_router.include_router(filter.router)
api_router.include_router(health.router)
api_router.include_router(nofication.router)
api_router.include_router(user.router)
api_router.include_router(job.router)
