from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from yuki.api.router import api_router
from yuki.core.config import get_settings
from yuki.core.exception_handlers import (
    business_exception_handler,
    http_exception_handler,
    request_validation_exception_handler,
    unhandled_exception_handler,
)
from yuki.core.exceptions import BusinessException
from yuki.core.middleware import RequestContextMiddleware
from yuki.infra.database import create_db_engine, create_session_factory
from yuki.infra.logging import configure_logging


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    configure_logging()
    settings = get_settings()
    engine = create_db_engine(str(settings.database_url))

    try:
        session_factory = create_session_factory(engine)
        app.state.db_session_factory = session_factory
        yield
    finally:
        await engine.dispose()


app = FastAPI(lifespan=lifespan)
app.add_middleware(RequestContextMiddleware)
app.add_exception_handler(BusinessException, business_exception_handler)
app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)
app.include_router(api_router)
