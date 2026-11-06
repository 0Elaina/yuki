from typing import Annotated, Self

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, StringConstraints, field_validator

from yuki.modules.characters.constants import (
    CHARACTER_BATCH_DELETE_MAX_SIZE,
    CHARACTER_NAME_MAX_LENGTH,
    CHARACTER_PERSONA_MAX_LENGTH,
)
from yuki.modules.characters.models import Character
from yuki.shared.type.field_type import NormalizedId
from yuki.shared.util.field_utils import (
    CREATED_ALIAS,
    STR_ID_DESCRIPTION,
    UPDATED_ALIAS,
    validate_unique_ids,
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
CharacterKeyword = Annotated[
    str, StringConstraints(strip_whitespace=True, max_length=CHARACTER_NAME_MAX_LENGTH)
]


class CharacterCreate(BaseModel):
    """创建角色请求"""

    model_config = ConfigDict(extra="forbid")
    name: CharacterName
    persona: CharacterPersona = ""


class CharacterDetail(BaseModel):
    """角色详情"""

    model_config = ConfigDict(extra="forbid", serialize_by_alias=True)
    id: str = Field(description=STR_ID_DESCRIPTION)
    name: str
    persona: str
    created_at: AwareDatetime = Field(serialization_alias=CREATED_ALIAS)
    updated_at: AwareDatetime = Field(serialization_alias=UPDATED_ALIAS)

    @classmethod
    def of(cls, character: Character) -> Self:
        return cls(
            id=str(character.id),
            name=character.name,
            persona=character.persona,
            created_at=character.created_at,
            updated_at=character.updated_at,
        )


class CharacterListItem(BaseModel):
    """角色列表项"""

    model_config = ConfigDict(extra="forbid", serialize_by_alias=True)
    id: str = Field(description=STR_ID_DESCRIPTION)
    name: str
    created_at: AwareDatetime = Field(serialization_alias=CREATED_ALIAS)
    updated_at: AwareDatetime = Field(serialization_alias=UPDATED_ALIAS)

    @classmethod
    def of(cls, character: Character) -> Self:
        return cls(
            id=str(character.id),
            name=character.name,
            created_at=character.created_at,
            updated_at=character.updated_at,
        )


class CharacterUpdate(BaseModel):
    """更新角色请求"""

    model_config = ConfigDict(extra="forbid")
    name: CharacterName
    persona: CharacterPersona


class CharacterBatchDelete(BaseModel):
    """批量删除角色请求"""

    model_config = ConfigDict(extra="forbid")

    ids: list[NormalizedId] = Field(min_length=1, max_length=CHARACTER_BATCH_DELETE_MAX_SIZE)

    @field_validator("ids", mode="after")
    @classmethod
    def validate_unique_ids(cls, value: list[int]) -> list[int]:
        return validate_unique_ids(value)
