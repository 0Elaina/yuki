import logging
from typing import cast

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from yuki.api.schemas import (
    ApiResponse,
    CommonApiCode,
    ValidationErrorData,
    ValidationErrorItem,
)
from yuki.core.exceptions import BusinessException

logger = logging.getLogger(__name__)


async def business_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """将业务异常转换为统一响应，保留其声明的 HTTP 状态。"""
    business_exception = cast(BusinessException, exc)
    body = ApiResponse[None].error(
        api_code=business_exception.api_code,
        data=None,
        message=business_exception.message,
    )
    return JSONResponse(
        status_code=business_exception.api_code.http_status,
        content=body.model_dump(mode="json"),
    )


async def request_validation_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    """只公开请求校验错误的位置、类型和说明。"""
    validation_exception = cast(RequestValidationError, exc)
    errors = [
        ValidationErrorItem(
            loc=list(error["loc"]),
            type=error["type"],
            message=error["msg"],
        )
        for error in validation_exception.errors()
    ]
    body = ApiResponse[ValidationErrorData].error(
        api_code=CommonApiCode.INVALID_REQUEST,
        data=ValidationErrorData(errors=errors),
        message=None,
    )
    return JSONResponse(
        status_code=CommonApiCode.INVALID_REQUEST.http_status,
        content=body.model_dump(mode="json"),
    )


async def http_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """统一框架 HTTP 错误正文，保留原状态和协议响应头。"""
    http_exception = cast(StarletteHTTPException, exc)
    if http_exception.status_code == CommonApiCode.MISSING_RESOURCE.http_status:
        code = CommonApiCode.MISSING_RESOURCE.code
        message = CommonApiCode.MISSING_RESOURCE.message
    elif http_exception.status_code == CommonApiCode.UNSUPPORTED_METHOD.http_status:
        code = CommonApiCode.UNSUPPORTED_METHOD.code
        message = CommonApiCode.UNSUPPORTED_METHOD.message
    else:
        code = "HTTP_ERROR"
        message = "请求处理失败"

    body = ApiResponse[None](code=code, message=message, data=None)
    return JSONResponse(
        status_code=http_exception.status_code,
        content=body.model_dump(mode="json"),
        headers=http_exception.headers,
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """记录未捕获异常的堆栈，仅向客户端公开通用错误提示。"""
    request_id = cast(str, getattr(request.state, "request_id", "-"))
    logger.error(
        "处理请求时发生未捕获异常：%s %s",
        request.method,
        request.url.path,
        exc_info=(type(exc), exc, exc.__traceback__),
        extra={"request_id": request_id},
    )
    body = ApiResponse[None].error(
        api_code=CommonApiCode.INTERNAL_ERROR,
        data=None,
        message=None,
    )
    return JSONResponse(
        status_code=CommonApiCode.INTERNAL_ERROR.http_status,
        content=body.model_dump(mode="json"),
        headers={"X-Request-ID": request_id},
    )
