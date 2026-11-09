from fastapi import APIRouter, status

from yuki.app.dependencies import SessionDep
from yuki.modules.conversations import service as conversation_service
from yuki.modules.conversations.schemas import ConversationCreate, ConversationDetail
from yuki.shared.api.response import ApiResponse

router = APIRouter(prefix="/api/v1/conversations", tags=["conversations"])


@router.post("", status_code=status.HTTP_201_CREATED, summary="创建会话")
async def create_conversation(
    body: ConversationCreate, session: SessionDep
) -> ApiResponse[ConversationDetail]:
    """创建会话"""
    detail = await conversation_service.create_conversation(session, character_id=body.character_id)
    return ApiResponse.success(detail)
