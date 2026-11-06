"""业务异常只表达业务码和可公开的消息，不依赖 HTTP 框架。"""

from yuki.shared.api.api_code import ApiCode


class BusinessException(Exception):
    def __init__(self, api_code: ApiCode, message: str | None = None) -> None:
        self.api_code = api_code
        self.message = api_code.message if message is None else message
        super().__init__(self.message)
