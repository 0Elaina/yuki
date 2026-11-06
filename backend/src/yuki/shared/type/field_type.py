from typing import Annotated

from pydantic import BeforeValidator, Field

from yuki.shared.util.field_utils import parse_str_id
from yuki.shared.util.sql_utils import BIGINT_MAX

NormalizedId = Annotated[
    int, Field(gt=0, le=BIGINT_MAX), BeforeValidator(parse_str_id, json_schema_input_type=str)
]
