from abc import ABC, abstractmethod
from app.schemas.job import JobCreate

class BaseParser(ABC):
    @abstractmethod
    async def fetch_jobs(self) -> list[JobCreate]:
        pass

