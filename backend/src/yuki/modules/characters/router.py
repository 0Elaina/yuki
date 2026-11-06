from fastapi import APIRouter, status

from yuki.app.dependencies import SessionDep
from yuki.modules.characters import service
from yuki.modules.characters.schemas import CharacterCreate, CharacterDetail
from yuki.shared.api.response import ApiResponse

router = APIRouter(prefix="/api/v1/characters", tags=["characters"])


@router.post(
    "",
    response_model=ApiResponse[CharacterDetail],
    status_code=status.HTTP_201_CREATED,
    summary="创建角色",
)
async def create_character(
    body: CharacterCreate, session: SessionDep
) -> ApiResponse[CharacterDetail]:
    """创建角色"""

    detail = await service.create_character(session, data=body)
    return ApiResponse.success(detail)
