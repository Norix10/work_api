import jwt
from jwt import InvalidTokenError, ExpiredSignatureError
from datetime import timedelta, timezone, datetime
from uuid import UUID
import secrets
from fastapi import HTTPException, status


from app.core.config import settings
from app.repository.user import UserRepository
from app.repository.refresh_token import RefreshRepository
from app.models.user import User
from app.models.refresh_token import RefreshToken
from app.schemas.auth import TelegramAuthRequest, AuthResponse


class AuthService:
    def __init__(self, user_repo: UserRepository, token_repo: RefreshRepository):
        self.user_repo = user_repo
        self.token_repo = token_repo

    def _create_access_token(self, user_id: UUID) -> str:
        payload = {
            "sub": str(user_id),
            "exp": datetime.now(timezone.utc)
            + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    def _create_refresh_token(self) -> str:
        return secrets.token_urlsafe(32)

    async def telegram_auth(self, data: TelegramAuthRequest) -> AuthResponse:
        user = await self.user_repo.get_by_telegram_id(data.telegram_id)
        if not user:
            user = await self.user_repo.create(
                User(
                    telegram_id=data.telegram_id,
                    username=data.username,
                )
            )
        access_token = self._create_access_token(user.id)
        refresh_token = self._create_refresh_token()

        await self.token_repo.create(
            RefreshToken(
                user_id=user.id,
                token=refresh_token,
                expires_at=datetime.utcnow() + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
            )
        )
        return AuthResponse(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    async def refresh_token(self, token: str) -> AuthResponse:
        taken_obj = await self.token_repo.get_by_token(token)

        if not taken_obj:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )

        if taken_obj.expires_at < datetime.now(timezone.utc):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired"
            )

        access_token = self._create_access_token(taken_obj.user_id)

        return AuthResponse(
            access_token=access_token,
            refresh_token=token,
        )

    async def logout(self, token: str) -> None:
        await self.token_repo.delete_by_token(token)
