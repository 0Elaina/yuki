from typing import Self

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field

from yuki.modules.conversations.models import Conversation
from yuki.shared.type.field_type import NormalizedId
from yuki.shared.util.field_utils import CREATED_ALIAS, STR_ID_DESCRIPTION, UPDATED_ALIAS


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
