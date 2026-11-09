from sqlalchemy.ext.asyncio import AsyncSession

from yuki.modules.characters import repository as character_repository
from yuki.modules.characters.api_code import CharacterApiCode
from yuki.modules.conversations import repository as conversation_repository
from yuki.modules.conversations.constants import DEFAULT_CONVERSATION_TITLE
from yuki.modules.conversations.schemas import ConversationDetail
from yuki.shared.exceptions import BusinessException


async def create_conversation(session: AsyncSession, character_id: int) -> ConversationDetail:
    """创建会话"""

    async with session.begin():
        character = await character_repository.find_character_by_id(
            session, character_id=character_id
        )
        if character is None:
            raise BusinessException(CharacterApiCode.CHARACTER_NOT_FOUND)
        conversation = await conversation_repository.save_conversation(
            session, character_id=character_id, title=DEFAULT_CONVERSATION_TITLE
        )
        detail = ConversationDetail.of(conversation)
    return detail
