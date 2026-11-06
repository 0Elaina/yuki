from typing import Final

STR_ID_DESCRIPTION: Final[str] = "数据库 BIGINT 转换的十进制字符串"
CREATED_ALIAS: Final[str] = "createdAt"
UPDATED_ALIAS: Final[str] = "updatedAt"


def parse_str_id(value: object) -> int:
    """解析字符串 ID"""

    if not isinstance(value, str):
        raise ValueError("ID 必须是十进制整数字符串")
    if not (value.isascii() and value.isdecimal()):
        raise ValueError("ID 必须是十进制整数字符串")
    return int(value)


def validate_unique_ids(value: list[int]) -> list[int]:
    """校验 ID 列表唯一性"""

    if len(value) != len(set(value)):
        raise ValueError("ID 列表不能包含重复值")
    return value
