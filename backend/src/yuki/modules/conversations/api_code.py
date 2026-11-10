from typing import Final

from fastapi import status

from yuki.shared.api.api_code import ApiCode


class ConversationApiCode:
    CONVERSATION_NOT_FOUND: Final[ApiCode] = ApiCode(
        status.HTTP_404_NOT_FOUND, "CONVERSATION_NOT_FOUND", "会话不存在"
    )
