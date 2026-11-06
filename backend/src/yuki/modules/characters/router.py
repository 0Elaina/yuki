from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, status
from fastapi_pagination import Page

from yuki.app.dependencies import SessionDep
from yuki.modules.characters import service
from yuki.modules.characters.schemas import (
    CharacterCreate,
    CharacterDetail,
    CharacterKeyword,
    CharacterListItem,
)
from yuki.shared.api.pagination import PageQuery
from yuki.shared.api.response import ApiResponse
from yuki.shared.util.sql_utils import BIGINT_MAX

router = APIRouter(prefix="/api/v1/characters", tags=["characters"])


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="创建角色",
)
async def create_character(
    body: CharacterCreate, session: SessionDep
) -> ApiResponse[CharacterDetail]:
    """创建角色"""

    detail = await service.create_character(session, data=body)
    return ApiResponse.success(detail)


@router.get("", summary="分页查询角色")
async def list_characters(
    session: SessionDep,
    params: Annotated[PageQuery, Depends()],
    keyword: Annotated[CharacterKeyword, Query(description="角色名称关键词")] = "",
) -> ApiResponse[Page[CharacterListItem]]:
    """分页查询角色列表"""

    page = await service.list_characters(session, params=params, keyword=keyword)
    return ApiResponse.success(page)


@router.get("/{character_id}", summary="查询角色详情")
async def get_character(
    character_id: Annotated[int, Path(gt=0, le=BIGINT_MAX)], session: SessionDep
) -> ApiResponse[CharacterDetail]:
    """查询角色详情"""

    detail = await service.get_character(session, character_id=character_id)
    return ApiResponse.success(detail)
