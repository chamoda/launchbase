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
from app.security import JWT_AUDIENCE_PLATFORM

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


def decode_access_token(access_token: str, audience: str) -> str:
    try:
        # Split Bearer token and get the actual token
        token_parts = access_token.split()
        if len(token_parts) != 2 or token_parts[0].lower() != "bearer":
            raise APIException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                code="INVALID_TOKEN_FORMAT",
                message="Token must be in 'Bearer <token>' format",
            )

        # `audience` pins the token to its issuing surface; a mismatch raises
        # jwt.InvalidAudienceError (a PyJWTError) and is rejected below.
        payload = jwt.decode(
            token_parts[1],
            settings.SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
            audience=audience,
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


async def get_current_user(session: DBSession, access_token: str, audience: str):
    if access_token:
        try:
            sub = decode_access_token(access_token, audience)
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


def build_http_user_dependency(audience: str, cookie_name: str):
    """Build a `get_current_http_user` dependency scoped to a surface.

    Each surface reads its own cookie and validates the token's audience, so a
    token issued elsewhere is rejected even when a cookie is present.
    """
    cookie_scheme = APIKeyCookie(name=cookie_name, auto_error=False)
    header_scheme = APIKeyHeader(name="Access-Token", auto_error=False)

    async def get_current_http_user(
        session: DBSession,
        access_token_cookie: str | None = Depends(cookie_scheme),
        access_token_header: str | None = Depends(header_scheme),
    ):
        # Header takes precedence over cookie when both are present.
        access_token = access_token_header or access_token_cookie or ""

        if not access_token:
            raise http_credentials_required_exception

        try:
            return await get_current_user(
                session=session, access_token=access_token, audience=audience
            )
        except (APIException, ResourceNotFoundException):
            # Convert specific errors to generic credentials exception for security
            raise http_credentials_exception
        except Exception:
            # Catch any unexpected errors and convert to credentials exception
            raise http_credentials_exception

    return get_current_http_user


# Platform surface: `access_token` cookie, platform-audience tokens.
get_current_http_user = build_http_user_dependency(
    audience=JWT_AUDIENCE_PLATFORM, cookie_name="access_token"
)

CurrentUser = Annotated[User, Depends(get_current_http_user)]
