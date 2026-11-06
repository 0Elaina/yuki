from sqlalchemy.ext.asyncio import AsyncSession

from yuki.modules.characters.models import Character


async def add_character(session: AsyncSession, name: str, persona: str) -> Character:
    """新增角色"""

    character = Character(name=name, persona=persona)
    session.add(character)
    await session.flush()
    return character
