"""不可变业务码与公共业务码常量。"""

from dataclasses import dataclass
from http import HTTPStatus
from typing import Final


@dataclass(frozen=True)
class ApiCode:
    http_status: HTTPStatus
    code: str
    message: str


class CommonApiCode:
    SUCCESS: Final = ApiCode(HTTPStatus.OK, "SUCCESS", "响应成功")
    BAD_REQUEST: Final = ApiCode(HTTPStatus.BAD_REQUEST, "BAD_REQUEST", "请求参数有误")
    NOT_FOUND: Final = ApiCode(HTTPStatus.NOT_FOUND, "NOT_FOUND", "请求的资源不存在")
    METHOD_NOT_ALLOWED: Final = ApiCode(
        HTTPStatus.METHOD_NOT_ALLOWED, "METHOD_NOT_ALLOWED", "HTTP 请求方法不支持"
    )
    CONFLICT: Final = ApiCode(HTTPStatus.CONFLICT, "CONFLICT", "资源状态冲突")
    UPLOAD_TOO_LARGE: Final = ApiCode(
        HTTPStatus.REQUEST_ENTITY_TOO_LARGE, "UPLOAD_TOO_LARGE", "上传文件或请求过大"
    )
    UNSUPPORTED_MEDIA_TYPE: Final = ApiCode(
        HTTPStatus.UNSUPPORTED_MEDIA_TYPE, "UNSUPPORTED_MEDIA_TYPE", "请求内容类型不支持"
    )
    PARAM_VALIDATION_FAILED: Final = ApiCode(
        HTTPStatus.UNPROCESSABLE_ENTITY, "PARAM_VALIDATION_FAILED", "参数校验未通过"
    )
    TOO_MANY_REQUESTS: Final = ApiCode(
        HTTPStatus.TOO_MANY_REQUESTS, "TOO_MANY_REQUESTS", "请求过于频繁，请稍后重试"
    )
    INTERNAL_SERVER_ERROR: Final = ApiCode(
        HTTPStatus.INTERNAL_SERVER_ERROR, "INTERNAL_SERVER_ERROR", "系统内部异常，请稍后重试"
    )
    SERVICE_UNAVAILABLE: Final = ApiCode(
        HTTPStatus.SERVICE_UNAVAILABLE, "SERVICE_UNAVAILABLE", "服务暂不可用，请稍后重试"
    )
