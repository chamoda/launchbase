from typing import Annotated

import jwt
from fastapi import Depends, status
from fastapi.security import APIKeyCookie, APIKeyHeader
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.config import settings
from app.database import DBSession
from app.exceptions import APIException, ResourceNotFoundException
from app.models import User

http_credentials_exception = APIException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    code="INVALID_TOKEN",
    message="Could not validate credentials",
)

http_credentials_required_exception = APIException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    code="CREDENTIALS_REQUIRED",
    message="Credentials required from cookie or access token",
)


def decode_access_token(access_token: str) -> str:
    try:
        # Split Bearer token and get the actual token
        token_parts = access_token.split()
        if len(token_parts) != 2 or token_parts[0].lower() != "bearer":
            raise APIException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                code="INVALID_TOKEN_FORMAT",
                message="Token must be in 'Bearer <token>' format",
            )

        payload = jwt.decode(
            token_parts[1], settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        sub = payload.get("sub")
        if not sub:
            raise APIException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                code="INVALID_TOKEN_PAYLOAD",
                message="Token payload missing required 'sub' field",
            )
        return sub
    except jwt.PyJWTError as e:
        raise APIException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="INVALID_TOKEN",
            message=f"JWT validation failed: {str(e)}",
        )
    except APIException:
        # Re-raise our custom exceptions
        raise


async def get_user_by_id(user_id: str, session: DBSession) -> User:
    try:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalars().first()
        if not user:
            raise ResourceNotFoundException("User not found")
        return user
    except SQLAlchemyError:
        raise APIException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            code="DATABASE_ERROR",
            message="Database query failed",
        )
    except ResourceNotFoundException:
        # Re-raise our custom exception
        raise


async def get_current_user(session: DBSession, access_token: str):
    if access_token:
        try:
            sub = decode_access_token(access_token)
            return await get_user_by_id(user_id=sub, session=session)
        except (APIException, ResourceNotFoundException):
            # Re-raise our custom exceptions
            raise
        except Exception:
            raise APIException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                code="AUTHENTICATION_FAILED",
                message="Authentication failed due to unexpected error",
            )


async def get_current_http_user(
    session: DBSession,
    access_token_cookie: str | None = Depends(
        APIKeyCookie(name="access_token", auto_error=False)
    ),
    access_token_header: str | None = Depends(
        APIKeyHeader(name="Access-Token", auto_error=False)
    ),
):
    access_token = ""
    if access_token_cookie:
        access_token = access_token_cookie
    if access_token_header:
        access_token = access_token_header

    if not access_token:
        raise http_credentials_required_exception

    try:
        return await get_current_user(session=session, access_token=access_token)
    except (APIException, ResourceNotFoundException):
        # Convert specific errors to generic credentials exception for security
        raise http_credentials_exception
    except Exception:
        # Catch any unexpected errors and convert to credentials exception
        raise http_credentials_exception


CurrentUser = Annotated[User, Depends(get_current_http_user)]
