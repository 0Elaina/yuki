from typing import Final

from fastapi import status

from yuki.shared.api.api_code import ApiCode


class CharacterApiCode:
    CHARACTER_NOT_FOUND: Final = ApiCode(
        status.HTTP_404_NOT_FOUND, "CHARACTER_NOT_FOUND", "角色不存在"
    )
