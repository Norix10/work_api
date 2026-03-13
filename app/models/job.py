from models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Boolean, Enum, Text
from sqlalchemy.dialects.postgresql import ARRAY
import enum

from app.models.enums.job_enum import JobRemote, JobLevel, JobSource

class Job(Base):
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    company: Mapped[str | None] = mapped_column(String(255), nullable=True)
    url: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    salary_min: Mapped[int | None] = mapped_column(Integer, nullable=True)
    salary_max: Mapped[int | None] = mapped_column(Integer, nullable=True)
    level: Mapped[JobLevel | None] = mapped_column(Enum(JobLevel), nullable=True)
    technologies: Mapped[list[str] | None] = mapped_column(ARRAY(String), nullable=True)
    remote_type: Mapped[JobRemote] = mapped_column(Enum(JobRemote), nullable=False)
    source: Mapped[JobSource] = mapped_column(Enum(JobSource), nullable=False)

    sent_jobs: Mapped[list["SentJob"]] = relationship(
        back_populates="job", cascade="all, delete-orphan"
    )


# title, company, url, decription, salary_min, max, level, technologies, remote, source, sent_jobs
