"""通过 FastAPI 异常处理器返回统一错误响应。"""

from collections.abc import Mapping
from typing import cast

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse

from yuki.shared.api.api_code import ApiCode, CommonApiCode
from yuki.shared.api.response import ApiResponse
from yuki.shared.exceptions import BusinessException

_HTTP_ERROR_CODES: dict[int, ApiCode] = {
    api_code.http_status: api_code
    for api_code in (
        CommonApiCode.BAD_REQUEST,
        CommonApiCode.NOT_FOUND,
        CommonApiCode.METHOD_NOT_ALLOWED,
        CommonApiCode.CONFLICT,
        CommonApiCode.UPLOAD_TOO_LARGE,
        CommonApiCode.UNSUPPORTED_MEDIA_TYPE,
        CommonApiCode.PARAM_VALIDATION_FAILED,
        CommonApiCode.TOO_MANY_REQUESTS,
        CommonApiCode.INTERNAL_SERVER_ERROR,
        CommonApiCode.SERVICE_UNAVAILABLE,
    )
}


def _error_response(
    api_code: ApiCode,
    message: str | None = None,
    headers: Mapping[str, str] | None = None,
) -> JSONResponse:
    return JSONResponse(
        status_code=api_code.http_status,
        content=ApiResponse.error(api_code, message).model_dump(mode="json"),
        headers=headers,
    )


async def handle_business_exception(request: Request, exc: Exception) -> JSONResponse:
    # Starlette 按注册的异常类型分发，回调签名统一接受 Exception。
    business_exc = cast(BusinessException, exc)
    return _error_response(business_exc.api_code, business_exc.message)


async def handle_request_validation(request: Request, exc: Exception) -> JSONResponse:
    return _error_response(CommonApiCode.PARAM_VALIDATION_FAILED)


async def handle_http_exception(request: Request, exc: Exception) -> JSONResponse:
    http_exc = cast(HTTPException, exc)
    api_code = _HTTP_ERROR_CODES.get(http_exc.status_code, CommonApiCode.INTERNAL_SERVER_ERROR)
    return _error_response(api_code, headers=http_exc.headers)


async def handle_unexpected_exception(request: Request, exc: Exception) -> JSONResponse:
    # Starlette 发送错误响应后重抛异常，堆栈由 Uvicorn 记录。
    return _error_response(CommonApiCode.INTERNAL_SERVER_ERROR)


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(BusinessException, handle_business_exception)
    app.add_exception_handler(RequestValidationError, handle_request_validation)
    app.add_exception_handler(HTTPException, handle_http_exception)
    app.add_exception_handler(Exception, handle_unexpected_exception)
