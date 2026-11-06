"""分页参数与统一维护的默认值、条数上限。"""

from typing import Final

from fastapi import Query
from fastapi_pagination import Params

DEFAULT_PAGE: Final = 1
DEFAULT_PAGE_SIZE: Final = 20
MAX_PAGE_SIZE: Final = 100


class PageQuery(Params):
    page: int = Query(DEFAULT_PAGE, ge=1, description="页码")
    size: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE, description="每页条数")
