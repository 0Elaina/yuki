from fastapi import APIRouter

from yuki.api.schemas import ApiResponse, CommonApiCode, ValidationErrorData

api_router = APIRouter(
    prefix="/api/v1",
    responses={
        CommonApiCode.INVALID_REQUEST.http_status: {
            "model": ApiResponse[ValidationErrorData],
            "description": CommonApiCode.INVALID_REQUEST.message,
        },
        CommonApiCode.INTERNAL_ERROR.http_status: {
            "model": ApiResponse[None],
            "description": CommonApiCode.INTERNAL_ERROR.message,
        },
    },
)
