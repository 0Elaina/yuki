from fastapi_pagination import Page
from fastapi_pagination.config import Config
from fastapi_pagination.ext.sqlalchemy import apaginate
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import load_only

from yuki.modules.characters.models import Character
from yuki.shared.api.pagination import PageQuery


async def add_character(session: AsyncSession, name: str, persona: str) -> Character:
    """新增角色"""

    character = Character(name=name, persona=persona)
    session.add(character)
    await session.flush()
    return character


async def find_character_by_id(session: AsyncSession, *, character_id: int) -> Character | None:
    """根据 ID 查询角色详情"""

    return await session.get(Character, character_id)


async def page_characters(
    session: AsyncSession, *, params: PageQuery, keyword: str
) -> Page[Character]:
    """分页查询角色"""

    stmt = select(Character).options(
        load_only(
            Character.id, Character.name, Character.created_at, Character.updated_at, raiseload=True
        )
    )
    if keyword:
        stmt = stmt.where(Character.name.icontains(keyword, autoescape=True))
    stmt = stmt.order_by(Character.id.desc())
    result = await apaginate(session, stmt, params=params, config=Config(page_cls=Page[Character]))
    return result


async def update_character(
    session: AsyncSession, *, character: Character, name: str, persona: str
) -> Character:
    """更新角色"""

    character.name = name
    character.persona = persona
    await session.flush()
    return character


async def delete_characters(session: AsyncSession, *, ids: list[int]) -> list[int]:
    """批量删除角色"""

    result = await session.execute(
        delete(Character).where(Character.id.in_(ids)).returning(Character.id)
    )
    return list(result.scalars().all())
