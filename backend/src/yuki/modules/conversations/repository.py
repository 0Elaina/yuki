from sqlalchemy.ext.asyncio import AsyncSession

from yuki.modules.conversations.models import Conversation


async def save_conversation(session: AsyncSession, character_id: int, title: str) -> Conversation:
    """保存会话"""

    conversation = Conversation(character_id=character_id, title=title)
    session.add(conversation)
    await session.flush()
    return conversation
