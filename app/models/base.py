import re
import uuid
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr


def camel_to_snake(name: str) -> str:
    snake = re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()
    return f"{snake}s"


class Base(DeclarativeBase):

    @declared_attr
    def __tablename__(cls) -> str:
        return camel_to_snake(cls.__name__)

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )
