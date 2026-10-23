from dataclasses import dataclass
from http import HTTPStatus
from typing import Self

from pydantic import BaseModel


@dataclass(frozen=True)
class ApiCode:
    http_status: HTTPStatus
    code: str
    message: str


class CommonApiCode:
    SUCCESS = ApiCode(HTTPStatus.OK, "SUCCESS", "响应成功")
    INVALID_REQUEST = ApiCode(
        HTTPStatus.UNPROCESSABLE_ENTITY, "INVALID_REQUEST", "请求参数无效"
    )
    MISSING_RESOURCE = ApiCode(HTTPStatus.NOT_FOUND, "MISSING_RESOURCE", "资源不存在")
    UNSUPPORTED_METHOD = ApiCode(
        HTTPStatus.METHOD_NOT_ALLOWED, "UNSUPPORTED_METHOD", "请求方法不受支持"
    )
    INTERNAL_ERROR = ApiCode(
        HTTPStatus.INTERNAL_SERVER_ERROR, "INTERNAL_ERROR", "服务器内部错误"
    )


class ApiResponse[T](BaseModel):
    code: str
    message: str
    data: T

    @classmethod
    def success(cls, data: T) -> Self:
        return cls(
            code=CommonApiCode.SUCCESS.code,
            message=CommonApiCode.SUCCESS.message,
            data=data,
        )

    @classmethod
    def error(cls, api_code: ApiCode, data: T, message: str | None) -> Self:
        return cls(
            code=api_code.code,
            message=message or api_code.message,
            data=data,
        )


class ValidationErrorItem(BaseModel):
    loc: list[str | int]
    type: str
    message: str


class ValidationErrorData(BaseModel):
    errors: list[ValidationErrorItem]
