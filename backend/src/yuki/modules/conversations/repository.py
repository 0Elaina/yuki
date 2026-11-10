from fastapi_pagination import Page
from fastapi_pagination.config import Config
from fastapi_pagination.ext.sqlalchemy import apaginate
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from yuki.modules.conversations.models import Conversation
from yuki.shared.api.pagination import PageQuery


async def save_conversation(session: AsyncSession, character_id: int, title: str) -> Conversation:
    """保存会话"""

    conversation = Conversation(character_id=character_id, title=title)
    session.add(conversation)
    await session.flush()
    return conversation


async def find_conversation_by_id(
    session: AsyncSession, *, conversation_id: int
) -> Conversation | None:
    """根据 ID 查询会话详情"""

    return await session.get(Conversation, conversation_id)


async def page_conversations(
    session: AsyncSession, *, character_id: int, params: PageQuery
) -> Page[Conversation]:
    """分页查询会话"""

    stmt = (
        select(Conversation)
        .where(Conversation.character_id == character_id)
        .order_by(Conversation.updated_at.desc(), Conversation.id.desc())
    )
    return await apaginate(session, stmt, params=params, config=Config(page_cls=Page[Conversation]))


async def delete_conversations(session: AsyncSession, *, ids: list[int]) -> list[int]:
    """批量删除会话并返回已删除的 ID 列表"""

    stmt = delete(Conversation).where(Conversation.id.in_(ids)).returning(Conversation.id)
    result = await session.execute(stmt)
    return list(result.scalars().all())
