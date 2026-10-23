from yuki.api.schemas import ApiCode


class BusinessException(Exception):
    """业务异常"""

    def __init__(self, api_code: ApiCode, message: str | None) -> None:
        self.api_code = api_code
        self.message = message or api_code.message
        super().__init__(self.message)
