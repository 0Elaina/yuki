"""组装 FastAPI 应用及原生 CORS 中间件。"""

import logging
from importlib.metadata import version

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.types import ASGIApp

from yuki.app.exception_handlers import register_exception_handlers
from yuki.app.lifespan import application_lifespan
from yuki.infrastructure.config import AppSettings
from yuki.modules.characters.router import router as characters_router
from yuki.modules.conversations.router import router as conversations_router
from yuki.shared.api.response import ApiResponse


def create_app() -> ASGIApp:
    settings = AppSettings.settings_cached()
    logging.basicConfig(
        level=settings.log_level,
        format="%(levelname)s %(name)s: %(message)s",
    )
    app = FastAPI(
        title="Yuki API",
        version=version("yuki"),
        lifespan=application_lifespan,
        responses={
            422: {"model": ApiResponse[None], "description": "请求参数校验失败"},
            500: {"model": ApiResponse[None], "description": "服务内部错误"},
        },
    )
    register_exception_handlers(app)
    app.include_router(characters_router)
    app.include_router(conversations_router)

    # 放在应用外层，使未处理异常的 500 响应也包含适用的 CORS 头。
    return CORSMiddleware(
        app,
        allow_origins=settings.cors_allow_origins,
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )
