from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from datetime import datetime, timezone
from app.repository.base import BaseRepository
from app.models.refresh_token import RefreshToken


class RefreshRepository(BaseRepository[RefreshToken]):
    def __init__(self, session: AsyncSession):
        super().__init__(RefreshToken, session)

    async def get_by_token(self, token: str) -> RefreshToken | None: 
        result = await self.session.execute(
            select(RefreshToken).where(RefreshToken.token == token)
        )
        return result.scalar_one_or_none()
    
    async def delete_by_token(self, token: str) -> None: 
        obj = await self.get_by_token(token) 
        if obj:
            await self.session.delete(obj)
            await self.session.commit()

    async def delete_expired(self) -> None:  
        await self.session.execute(
            delete(RefreshToken).where(
                RefreshToken.expires_at < datetime.now(timezone.utc)
            )
        )
        await self.session.commit()