from fastapi_pagination import Page
from sqlalchemy.ext.asyncio import AsyncSession

from yuki.modules.characters import repository as character_repository
from yuki.modules.characters.api_code import CharacterApiCode
from yuki.modules.conversations import repository as conversation_repository
from yuki.modules.conversations.api_code import ConversationApiCode
from yuki.modules.conversations.constants import DEFAULT_CONVERSATION_TITLE
from yuki.modules.conversations.schemas import ConversationDetail, MessageDetail, MessageHistory
from yuki.shared.api.pagination import PageQuery
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


async def get_conversation(session: AsyncSession, *, conversation_id: int) -> ConversationDetail:
    """根据 ID 获取会话详情"""

    async with session.begin():
        conversation = await conversation_repository.find_conversation_by_id(
            session, conversation_id=conversation_id
        )
        if conversation is None:
            raise BusinessException(ConversationApiCode.CONVERSATION_NOT_FOUND)
        detail = ConversationDetail.of(conversation)
    return detail


async def list_conversations(
    session: AsyncSession, *, character_id: int, params: PageQuery
) -> Page[ConversationDetail]:
    """分页查询角色会话列表"""

    async with session.begin():
        page = await conversation_repository.page_conversations(
            session, character_id=character_id, params=params
        )
        items = [ConversationDetail.of(c) for c in page.items]
    return Page[ConversationDetail](
        items=items, total=page.total, page=page.page, size=page.size, pages=page.pages
    )


async def delete_conversations(session: AsyncSession, *, ids: list[int]) -> int:
    """批量删除会话, 任一不存在则回滚并报错"""

    async with session.begin():
        deleted_ids = await conversation_repository.delete_conversations(session, ids=ids)
        if len(deleted_ids) != len(ids):
            raise BusinessException(ConversationApiCode.CONVERSATION_NOT_FOUND)
    return len(deleted_ids)


async def get_message_history(
    session: AsyncSession, *, conversation_id: int, before_id: int | None, size: int
) -> MessageHistory:
    """按消息 ID 游标分页读取会话历史"""

    async with session.begin():
        conversation = await conversation_repository.find_conversation_by_id(
            session, conversation_id=conversation_id
        )
        if conversation is None:
            raise BusinessException(ConversationApiCode.CONVERSATION_NOT_FOUND)
        rows = await conversation_repository.list_messages_before(
            session, conversation_id=conversation_id, before_id=before_id, limit=size + 1
        )
        has_more = len(rows) > size
        page_rows = rows[:size]
        items = [MessageDetail.of(row) for row in page_rows]
        next_before_id = str(page_rows[-1].id) if has_more else None

    return MessageHistory(items=items, next_before_id=next_before_id)
