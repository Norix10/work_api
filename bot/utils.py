from app.core.config import settings
from bot.storage import user_tokens
import httpx


async def get_or_refresh_token(telegram_id: int) -> str | None:
    token = user_tokens.get(telegram_id)
    if not token:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                f"{settings.API_URL}/api/v1/auth/telegram",
                json={"telegram_id": telegram_id},
            )
        if response.status_code == 200:
            token = response.json()["access_token"]
            user_tokens[telegram_id] = token
    return token
