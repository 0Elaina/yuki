from typing import Annotated

from pydantic import BeforeValidator, Field

from yuki.shared.constants.number import IntBoundary
from yuki.shared.util.field_utils import parse_str_id

NormalizedId = Annotated[
    int,
    Field(gt=0, le=IntBoundary.INT_MAX),
    BeforeValidator(parse_str_id, json_schema_input_type=str),
]
