from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Identity, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from yuki.infrastructure.database.base import Base
from yuki.shared.util.time_utils import utc_now


class Character(Base):
    __tablename__ = "characters"

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    persona: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utc_now
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utc_now, onupdate=utc_now
    )
