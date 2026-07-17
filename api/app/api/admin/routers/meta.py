from fastapi import APIRouter, Response, status
from sqlalchemy import select, text

from app.api.admin.schemas import AuthRequest, AuthResponse
from app.config import settings
from app.database import DBSession
from app.exceptions import APIException
from app.logging import logging
from app.models import User
from app.schemas import HealthCheckResponse, MessageResponse
from app.security import (
    JWT_AUDIENCE_ADMIN,
    generate_jwt_token,
    verify_password,
)

# Admin sessions use a dedicated cookie so an admin can hold platform and admin
# sessions at once without one overwriting the other.
ADMIN_COOKIE_NAME = "admin_access_token"

router = APIRouter()


@router.get("/health", tags=["meta"])
async def health(session: DBSession, response: Response) -> HealthCheckResponse:
    try:
        # Check database connectivity
        await session.execute(text("SELECT 1"))
        return HealthCheckResponse(status="healthy")

    except Exception as e:
        # Log error internally but don't expose details
        logging.error(f"Admin health check failed: {e}")
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return HealthCheckResponse(status="unhealthy")


@router.post("/auth", tags=["auth"])
async def auth(
    auth_request: AuthRequest, session: DBSession, response: Response
) -> AuthResponse:
    result = await session.execute(
        select(User).where(
            User.email == auth_request.email.lower(),
        )
    )
    user = result.scalars().first()

    # Only admins may authenticate against the admin surface. Non-admins get the
    # same generic error as bad credentials so account state isn't disclosed.
    if user and user.is_admin and user.password is not None:
        if verify_password(auth_request.password, user.password):
            access_token = generate_jwt_token(
                {"sub": str(user.id)}, audience=JWT_AUDIENCE_ADMIN
            )
            response.set_cookie(
                key=ADMIN_COOKIE_NAME,
                value=f"Bearer {access_token}",
                samesite="lax",
                secure=settings.SECURE_COOKIE,
                httponly=True,
                max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # Convert to seconds
            )
            return AuthResponse(access_token=access_token)
    raise APIException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        code="INVALID_CREDENTIALS",
        message="Incorrect username or password",
    )


@router.post("/logout", tags=["auth"])
async def logout(response: Response) -> MessageResponse:
    response.delete_cookie(ADMIN_COOKIE_NAME)
    return MessageResponse(message="Successfully logged out")
