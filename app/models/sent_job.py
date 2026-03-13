from models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, UniqueConstraint
import uuid

class SentJob(Base):
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    job_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)

    __table_args__ = (
        UniqueConstraint("user_id", "job_id", name="uq_user_job"),
    )

    # Relationships
    user: Mapped["User"] = relationship(back_populates="sent_jobs")
    job: Mapped["Job"] = relationship(back_populates="sent_jobs")