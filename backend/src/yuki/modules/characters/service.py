from fastapi_pagination import Page
from sqlalchemy.ext.asyncio import AsyncSession

from yuki.modules.characters import repository
from yuki.modules.characters.api_code import CharacterApiCode
from yuki.modules.characters.models import Character
from yuki.modules.characters.schemas import (
    CharacterCreate,
    CharacterDetail,
    CharacterListItem,
    CharacterUpdate,
)
from yuki.shared.api.pagination import PageQuery
from yuki.shared.exceptions import BusinessException


async def create_character(session: AsyncSession, *, data: CharacterCreate) -> CharacterDetail:
    """创建角色"""

    async with session.begin():
        character: Character = await repository.add_character(
            session, name=data.name, persona=data.persona
        )
        detail: CharacterDetail = CharacterDetail.of(character)
    return detail


async def get_character(session: AsyncSession, *, character_id: int) -> CharacterDetail:
    """根据 ID 获取获取角色详情"""

    async with session.begin():
        character = await repository.find_character_by_id(session, character_id=character_id)
        if character is None:
            raise BusinessException(CharacterApiCode.CHARACTER_NOT_FOUND)
        detail: CharacterDetail = CharacterDetail.of(character)
    return detail


async def list_characters(
    session: AsyncSession, *, params: PageQuery, keyword: str
) -> Page[CharacterListItem]:
    """分页查询角色列表"""

    async with session.begin():
        page = await repository.page_characters(session, params=params, keyword=keyword)
        items = [CharacterListItem.of(c) for c in page.items]
    return Page[CharacterListItem](
        items=items, total=page.total, page=page.page, size=page.size, pages=page.pages
    )


async def update_character(
    session: AsyncSession, *, character_id: int, data: CharacterUpdate
) -> CharacterDetail:
    """更新角色"""

    async with session.begin():
        character = await repository.find_character_by_id(session, character_id=character_id)
        if character is None:
            raise BusinessException(CharacterApiCode.CHARACTER_NOT_FOUND)
        character = await repository.update_character(
            session, character=character, name=data.name, persona=data.persona
        )
        detail = CharacterDetail.of(character)
    return detail


async def delete_characters(session: AsyncSession, *, ids: list[int]) -> None:
    """批量删除角色"""

    async with session.begin():
        deleted_ids = await repository.delete_characters(session, ids=ids)
        if len(deleted_ids) != len(ids):
            raise BusinessException(CharacterApiCode.CHARACTER_NOT_FOUND)
