from sqlalchemy.ext.asyncio import AsyncSession

from yuki.modules.characters.models import Character
from yuki.modules.characters.repository import add_character
from yuki.modules.characters.schemas import CharacterCreate, CharacterDetail


async def create_character(session: AsyncSession, *, data: CharacterCreate) -> CharacterDetail:
    """创建角色"""

    async with session.begin():
        character: Character = await add_character(session, name=data.name, persona=data.persona)
        detail: CharacterDetail = CharacterDetail.of(character)
    return detail
