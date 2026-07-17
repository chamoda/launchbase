from fastapi import (
    APIRouter,
)

from app.api.platform.access import CurrentUser
from app.api.platform.schemas import UserResponse

router = APIRouter()


@router.get("/users/self", tags=["users"])
async def get_current_user(current_user: CurrentUser) -> UserResponse:
    return UserResponse.model_validate(current_user)
