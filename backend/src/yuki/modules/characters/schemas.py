from typing import Annotated

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, StringConstraints

from yuki.modules.characters.constants import (
    CHARACTER_NAME_MAX_LENGTH,
    CHARACTER_PERSONA_MAX_LENGTH,
)

CharacterName = Annotated[
    str,
    StringConstraints(
        strict=True, strip_whitespace=True, min_length=1, max_length=CHARACTER_NAME_MAX_LENGTH
    ),
]
CharacterPersona = Annotated[
    str, StringConstraints(strict=True, max_length=CHARACTER_PERSONA_MAX_LENGTH)
]


class CharacterCreate(BaseModel):
    """创建角色请求"""

    model_config = ConfigDict(extra="forbid")
    name: CharacterName
    persona: CharacterPersona = ""


class CharacterDetail(BaseModel):
    """角色详情"""

    model_config = ConfigDict(extra="forbid", serialize_by_alias=True)
    id: str = Field(description="数据库 BIGINT 转换的十进制字符串")
    name: str
    persona: str
    created_at: AwareDatetime = Field(serialization_alias="createdAt")
    updated_at: AwareDatetime = Field(serialization_alias="updatedAt")
