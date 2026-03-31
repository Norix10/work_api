from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Boolean, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import ARRAY
from app.models.job import JobLevel, JobRemote
import uuid

class Filter(Base):
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    technologies: Mapped[list[str] | None] = mapped_column(ARRAY(String), nullable=True)
    level: Mapped[JobLevel | None] = mapped_column(Enum(JobLevel), nullable=True)
    salary_min: Mapped[int | None] = mapped_column(Integer, nullable=True)
    remote_type: Mapped[JobRemote] = mapped_column(Enum(JobRemote), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    user: Mapped["User"] = relationship(back_populates="filters")