from typing import Self

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, field_validator

from yuki.modules.conversations.constants import CONVERSATION_BATCH_DELETE_MAX_SIZE
from yuki.modules.conversations.models import Conversation
from yuki.shared.type.field_type import NormalizedId
from yuki.shared.util.field_utils import (
    CREATED_ALIAS,
    STR_ID_DESCRIPTION,
    UPDATED_ALIAS,
    validate_unique_ids,
)


class ConversationCreate(BaseModel):
    """创建会话请求"""

    model_config = ConfigDict(extra="forbid", serialize_by_alias=True)
    character_id: NormalizedId = Field(alias="characterId")


class ConversationDetail(BaseModel):
    """会话详情"""

    model_config = ConfigDict(extra="forbid", serialize_by_alias=True)
    id: str = Field(description=STR_ID_DESCRIPTION)
    character_id: str = Field(description=STR_ID_DESCRIPTION, serialization_alias="characterId")
    title: str
    created_at: AwareDatetime = Field(serialization_alias=CREATED_ALIAS)
    updated_at: AwareDatetime = Field(serialization_alias=UPDATED_ALIAS)

    @classmethod
    def of(cls, conversation: Conversation) -> Self:
        return cls(
            id=str(conversation.id),
            character_id=str(conversation.character_id),
            title=conversation.title,
            created_at=conversation.created_at,
            updated_at=conversation.updated_at,
        )


class ConversationBatchDelete(BaseModel):
    """批量删除会话请求"""

    model_config = ConfigDict(extra="forbid")
    ids: list[NormalizedId] = Field(min_length=1, max_length=CONVERSATION_BATCH_DELETE_MAX_SIZE)

    @field_validator("ids", mode="after")
    @classmethod
    def validate_unique_ids(cls, value: list[int]) -> list[int]:
        return validate_unique_ids(value)
