from enum import StrEnum
from typing import Final

CONVERSATION_TITLE_MAX_LENGTH: Final[int] = 40
DEFAULT_CONVERSATION_TITLE: Final[str] = "新会话"
CONVERSATION_BATCH_DELETE_MAX_SIZE: Final[int] = 100


class MessageRole(StrEnum):
    """消息发送者角色"""

    USER = "user"
    ASSISTANT = "assistant"
