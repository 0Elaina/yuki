from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, Identity, Index, String
from sqlalchemy.orm import Mapped, mapped_column

from yuki.infrastructure.database.base import Base
from yuki.shared.util.time_utils import utc_now


class Conversation(Base):
    """会话实体"""

    __tablename__ = "conversations"
    __table_args__ = (Index(None, "character_id", "updated_at", "id"),)

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True)
    character_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            "characters.id", ondelete="CASCADE", name="fk_conversations_character_id_characters"
        ),
        nullable=False,
    )
    title: Mapped[str] = mapped_column(String(64), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utc_now
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utc_now, onupdate=utc_now
    )
