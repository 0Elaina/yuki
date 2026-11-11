from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, status
from fastapi_pagination import Page

from yuki.app.dependencies import SessionDep
from yuki.modules.conversations import service as conversation_service
from yuki.modules.conversations.schemas import (
    ConversationBatchDelete,
    ConversationCreate,
    ConversationDetail,
    MessageHistory,
)
from yuki.shared.api.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE, PageQuery
from yuki.shared.api.response import ApiResponse
from yuki.shared.constants.number import IntBoundary
from yuki.shared.type.field_type import NormalizedId

router = APIRouter(prefix="/api/v1/conversations", tags=["conversations"])


@router.post("", status_code=status.HTTP_201_CREATED, summary="创建会话")
async def create_conversation(
    body: ConversationCreate, session: SessionDep
) -> ApiResponse[ConversationDetail]:
    """创建会话"""

    detail = await conversation_service.create_conversation(session, character_id=body.character_id)
    return ApiResponse.success(detail)


@router.get("/{conversation_id}", summary="查询会话详情")
async def get_conversation(
    conversation_id: Annotated[int, Path(gt=0, le=IntBoundary.INT_MAX)], session: SessionDep
) -> ApiResponse[ConversationDetail]:
    """查询会话详情"""

    detail = await conversation_service.get_conversation(session, conversation_id=conversation_id)
    return ApiResponse.success(detail)


@router.get("", summary="分页查询会话")
async def list_conversations(
    session: SessionDep,
    character_id: Annotated[NormalizedId, Query(alias="characterId", description="角色ID")],
    params: Annotated[PageQuery, Depends()],
) -> ApiResponse[Page[ConversationDetail]]:
    """分页查询会话列表"""

    page = await conversation_service.list_conversations(
        session, character_id=character_id, params=params
    )
    return ApiResponse.success(page)


@router.post("/batch-delete", summary="批量删除会话")
async def batch_delete_conversations(
    body: ConversationBatchDelete, session: SessionDep
) -> ApiResponse[int]:
    """批量删除会话"""

    deleted_count = await conversation_service.delete_conversations(session, ids=body.ids)
    return ApiResponse.success(deleted_count)


@router.delete("/{conversation_id}", summary="根据ID删除会话")
async def delete_conversation(
    conversation_id: Annotated[int, Path(gt=0, le=IntBoundary.INT_MAX)], session: SessionDep
) -> ApiResponse[None]:
    """根据ID删除会话"""

    await conversation_service.delete_conversations(session, ids=[conversation_id])
    return ApiResponse.success()


@router.get("/{conversation_id}/messages", summary="查询会话历史消息")
async def get_message_history(
    conversation_id: Annotated[int, Path(gt=0, le=IntBoundary.INT_MAX)],
    session: SessionDep,
    before_id: Annotated[NormalizedId | None, Query(alias="beforeId")] = None,
    size: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,
) -> ApiResponse[MessageHistory]:
    """查询会话历史消息"""
    history = await conversation_service.get_message_history(
        session, conversation_id=conversation_id, before_id=before_id, size=size
    )
    return ApiResponse.success(history)
