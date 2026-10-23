import logging
from contextvars import ContextVar
from logging.config import dictConfig

request_id_var: ContextVar[str] = ContextVar("request_id", default="-")


class RequestIdFilter(logging.Filter):
    """补充当前请求 ID，保留日志显式提供的值。"""

    def filter(self, record: logging.LogRecord) -> bool:
        record.__dict__.setdefault("request_id", request_id_var.get())
        return True


def configure_logging() -> None:
    """配置应用文本日志，由应用生命周期启动阶段调用。"""
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "standard": {
                    "format": (
                        "%(asctime)s %(levelname)s %(name)s "
                        "[request_id=%(request_id)s] %(message)s"
                    ),
                },
            },
            "filters": {
                "request_id": {
                    "()": RequestIdFilter,
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "level": "INFO",
                    "stream": "ext://sys.stderr",
                    "formatter": "standard",
                    "filters": ["request_id"],
                },
            },
            "root": {
                "level": "INFO",
                "handlers": ["console"],
            },
        }
    )
