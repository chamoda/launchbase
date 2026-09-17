import uuid

from fastapi import APIRouter, Query, status

from app.api.internal.access import CurrentInternalUser
from app.api.internal.schemas import (
    InternalUserResponse,
    UserChangePasswordRequest,
    UserCreateRequest,
    UsersListResponse,
    UserUpdateRequest,
)
from app.database import DBSession
from app.services.users import UserService

router = APIRouter()


@router.get("/users/self", tags=["users"])
async def get_current_internal_user(
    current_user: CurrentInternalUser,
) -> InternalUserResponse:
    return InternalUserResponse.model_validate(current_user)


@router.get("/users", tags=["users"])
async def user_list(
    current_user: CurrentInternalUser,
    session: DBSession,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
) -> UsersListResponse:
    users, total = await UserService(session).list_users(limit=limit, offset=offset)
    return UsersListResponse(
        items=[InternalUserResponse.model_validate(u) for u in users],
        total=total,
        limit=limit,
        offset=offset,
    )


@router.post("/users", status_code=status.HTTP_201_CREATED, tags=["users"])
async def user_create(
    current_user: CurrentInternalUser,
    session: DBSession,
    data: UserCreateRequest,
) -> InternalUserResponse:
    user = await UserService(session).create_user(**data.model_dump())
    await session.commit()
    return InternalUserResponse.model_validate(user)


@router.patch("/users/{user_id}", tags=["users"])
async def user_update(
    current_user: CurrentInternalUser,
    session: DBSession,
    user_id: uuid.UUID,
    data: UserUpdateRequest,
) -> InternalUserResponse:
    user = await UserService(session).update_user(
        user_id, data.model_dump(exclude_unset=True)
    )
    await session.commit()
    return InternalUserResponse.model_validate(user)


@router.post(
    "/users/{user_id}/change-password",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["users"],
)
async def user_change_password(
    current_user: CurrentInternalUser,
    session: DBSession,
    user_id: uuid.UUID,
    data: UserChangePasswordRequest,
) -> None:
    await UserService(session).change_password(user_id, data.password)
    await session.commit()


@router.delete(
    "/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["users"]
)
async def user_delete(
    current_user: CurrentInternalUser,
    session: DBSession,
    user_id: uuid.UUID,
) -> None:
    await UserService(session).delete_user(user_id)
    await session.commit()
