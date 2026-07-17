from datetime import UTC
from typing import Annotated, Any

from pydantic import (
    AwareDatetime,
    BaseModel,
    ConfigDict,
    WrapSerializer,
)

DateTime = Annotated[
    AwareDatetime,
    WrapSerializer(
        lambda v, nxt: nxt(v.astimezone(UTC)).replace("+00:00", "Z"),
        when_used="json",
    ),
]


class Model(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, from_attributes=True)


class MessageResponse(Model):
    message: str


class ErrorDetail(Model):
    code: str
    message: str
    field: str | None = None
    details: dict[str, Any] | None = None


class ErrorResponse(Model):
    error: ErrorDetail


class HealthCheckResponse(Model):
    status: str  # "healthy" or "unhealthy"
