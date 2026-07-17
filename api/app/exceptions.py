from typing import Optional

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse


class APIException(HTTPException):
    """Custom exception rendered in FastAPI's validation-error shape.

    The body mirrors what Pydantic/FastAPI emit for a 422 so the frontend can
    handle every error the same way — mapping each entry to a form field via
    its `loc`:

        {"detail": [{"type": <code>, "loc": ["body", <field>], "msg": <message>}]}

    When an error isn't tied to a specific input field, `loc` is just ["body"]
    and the frontend surfaces it as a form-level error.
    """

    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
        field: Optional[str] = None,
    ):
        self.code = code
        self.message = message
        self.field = field
        super().__init__(status_code=status_code, detail=message)

    def to_response(self) -> JSONResponse:
        loc = ["body", self.field] if self.field else ["body"]
        error = {
            "type": self.code.lower(),
            "loc": loc,
            "msg": self.message,
        }
        return JSONResponse(status_code=self.status_code, content={"detail": [error]})


class ResourceNotFoundException(APIException):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            code="RESOURCE_NOT_FOUND",
            message=message,
        )


class ValidationException(APIException):
    def __init__(self, message: str, field: Optional[str] = None):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            code="VALIDATION_ERROR",
            message=message,
            field=field,
        )


class ConflictException(APIException):
    def __init__(self, message: str, field: Optional[str] = None):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            code="CONFLICT",
            message=message,
            field=field,
        )
