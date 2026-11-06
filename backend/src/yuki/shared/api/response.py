"""普通 JSON API 的三字段响应。"""

from __future__ import annotations

from typing import Self

from pydantic import BaseModel, ConfigDict

from yuki.shared.api.api_code import ApiCode, CommonApiCode


class ApiResponse[T](BaseModel):
    model_config = ConfigDict(frozen=True)

    data: T | None
    code: str
    message: str

    @classmethod
    def success(cls, data: T | None = None) -> Self:
        return cls(
            data=data,
            code=CommonApiCode.SUCCESS.code,
            message=CommonApiCode.SUCCESS.message,
        )

    @classmethod
    def error(cls, api_code: ApiCode, message: str | None = None) -> ApiResponse[None]:
        return ApiResponse[None](
            data=None,
            code=api_code.code,
            message=api_code.message if message is None else message,
        )
