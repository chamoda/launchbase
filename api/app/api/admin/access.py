from typing import Annotated

from fastapi import Depends, status

from app.api.platform.access import build_http_user_dependency
from app.exceptions import APIException
from app.models import User
from app.security import JWT_AUDIENCE_ADMIN

http_admin_required_exception = APIException(
    status_code=status.HTTP_403_FORBIDDEN,
    code="ADMIN_REQUIRED",
    message="Admin privileges required",
)

# Admin surface: `admin_access_token` cookie, admin-audience tokens. A platform
# token (different audience, different cookie) never resolves a user here.
get_current_http_user = build_http_user_dependency(
    audience=JWT_AUDIENCE_ADMIN, cookie_name="admin_access_token"
)


async def get_current_admin_user(
    user: Annotated[User, Depends(get_current_http_user)],
) -> User:
    # Token audience already restricts callers to the admin surface; the flag is
    # a second gate so a non-admin who somehow holds an admin-audience token
    # (e.g. a stale grant) is still refused.
    if not user.is_admin:
        raise http_admin_required_exception
    return user


CurrentAdminUser = Annotated[User, Depends(get_current_admin_user)]
