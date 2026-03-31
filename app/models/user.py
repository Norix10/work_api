from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, BigInteger, Boolean, Enum

from app.models.enums.user_enum import UserRole

class User(Base):
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    username: Mapped[str | None] = mapped_column(String(255), nullable=True)  
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.user, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    filters: Mapped[list["Filter"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    sent_jobs: Mapped[list["SentJob"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    notification_settings: Mapped["NotificationSettings"] = relationship(back_populates="user", uselist=False, cascade="all, delete-orphan")
    refresh_tokens: Mapped[list["RefreshToken"]] = relationship(back_populates="user", cascade="all, delete-orphan")