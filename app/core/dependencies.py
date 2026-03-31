import jwt
from jwt import InvalidTokenError
from uuid import UUID
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_async_session
from app.core.config import settings
from app.repository.user import UserRepository
from app.repository.job import JobRepository
from app.repository.filter import FilterRepository
from app.repository.sent_job import SentJobRepository
from app.repository.refresh_token import RefreshRepository
from app.services.auth import AuthService
from app.services.user import UserService
from app.services.job import JobService
from app.services.filter import FilterService
from app.models.user import User

bearer_scheme = HTTPBearer()


async def get_user_repo(
    session: AsyncSession = Depends(get_async_session),
) -> UserRepository:
    return UserRepository(session)


async def get_job_repo(
    session: AsyncSession = Depends(get_async_session),
) -> JobRepository:
    return JobRepository(session)


async def get_filter_repo(
    session: AsyncSession = Depends(get_async_session),
) -> FilterRepository:
    return FilterRepository(session)


async def get_sent_job_repo(
    session: AsyncSession = Depends(get_async_session),
) -> SentJobRepository:
    return SentJobRepository(session)


async def get_refresh_token_repo(
    session: AsyncSession = Depends(get_async_session),
) -> RefreshRepository:
    return RefreshRepository(session)


async def get_auth_service(
    user_repo: UserRepository = Depends(get_user_repo),
    token_repo: RefreshRepository = Depends(get_refresh_token_repo),
) -> AuthService:
    return AuthService(user_repo=user_repo, token_repo=token_repo)


async def get_user_service(
    user_repo: UserRepository = Depends(get_user_repo),
) -> UserService:
    return UserService(user_repo=user_repo)


async def get_filter_service(
    filter_repo: FilterRepository = Depends(get_filter_repo),
) -> FilterService:
    return FilterService(filter_repo=filter_repo)


async def get_job_service(
    job_repo: JobRepository = Depends(get_job_repo),
    filter_repo: FilterRepository = Depends(get_filter_repo),
) -> JobService:
    return JobService(job_repo=job_repo, filter_repo=filter_repo)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    user_repo: UserRepository = Depends(get_user_repo),
) -> User:
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        user_id: str = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

    user = await user_repo.get_by_id(UUID(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User is inactive"
        )

    return user


async def get_current_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin only")
    return current_user
