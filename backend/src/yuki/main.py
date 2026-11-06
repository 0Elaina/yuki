"""yuki-api 命令入口。"""

import uvicorn

from yuki.infrastructure.config import SOURCE_DIR, AppSettings


def main() -> None:
    settings = AppSettings.settings_cached()
    uvicorn.run(
        "yuki.app.factory:create_app",
        factory=True,
        host=settings.http_host,
        port=settings.http_port,
        reload=settings.http_reload,
        reload_dirs=[str(SOURCE_DIR)] if settings.http_reload else None,
        log_level=settings.log_level.lower(),
    )
