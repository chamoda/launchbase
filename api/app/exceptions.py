from typing import Any, Dict, Optional

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

from app.schemas import ErrorDetail, ErrorResponse


class APIException(HTTPException):
    """Custom exception that returns consistent error format"""

    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
        field: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        self.code = code
        self.message = message
        self.field = field
        self.details = details
        super().__init__(status_code=status_code, detail=message)

    def to_response(self) -> JSONResponse:
        error_detail = ErrorDetail(
            code=self.code, message=self.message, field=self.field, details=self.details
        )
        error_response = ErrorResponse(error=error_detail)
        return JSONResponse(
            status_code=self.status_code, content=error_response.model_dump()
        )


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
