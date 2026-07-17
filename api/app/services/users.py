import uuid
from collections.abc import Sequence
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import ConflictException, ResourceNotFoundException
from app.models import User
from app.security import hash_password


class UserService:
    """Business logic for user records.

    Holds the DB session so callers pass it once and then issue user operations
    without threading the session through every call.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def list_users(
        self,
        *,
        limit: int = 50,
        offset: int = 0,
    ) -> tuple[Sequence[User], int]:
        """Return a page of users, newest first.

        Returns the page of users together with the total matching count so
        callers can render pagination controls without a second query
        round-trip on the caller side.
        """
        total = await self.session.scalar(select(func.count()).select_from(User))

        result = await self.session.execute(
            select(User).order_by(User.created_at.desc()).limit(limit).offset(offset)
        )
        return result.scalars().all(), total or 0

    async def get_user(self, user_id: uuid.UUID) -> User:
        """Return a single user or raise 404."""
        result = await self.session.execute(select(User).where(User.id == user_id))
        user = result.scalars().first()
        if user is None:
            raise ResourceNotFoundException("User not found")
        return user

    async def create_user(
        self,
        *,
        first_name: str,
        last_name: str,
        email: str,
        password: str | None = None,
        is_admin: bool = False,
        is_active: bool = True,
    ) -> User:
        """Create a user, rejecting a duplicate email with 409."""
        email = email.lower()
        await self._ensure_email_available(email)

        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=hash_password(password) if password else None,
            is_admin=is_admin,
            is_active=is_active,
        )
        self.session.add(user)
        await self.session.flush()
        return user

    async def update_user(self, user_id: uuid.UUID, changes: dict[str, Any]) -> User:
        """Apply a partial (PATCH) update to a user.

        Only keys present in `changes` are touched. A null for any column is
        treated as "leave unchanged" so a non-nullable field is never blanked.
        Password is intentionally not updatable here — use `change_password`.
        """
        changes.pop("password", None)
        user = await self.get_user(user_id)

        if changes.get("email") is not None:
            email = changes["email"].lower()
            changes["email"] = email
            if email != user.email:
                await self._ensure_email_available(email, exclude_id=user.id)

        for field, value in changes.items():
            if value is not None:
                setattr(user, field, value)

        await self.session.flush()
        return user

    async def change_password(self, user_id: uuid.UUID, password: str) -> User:
        """Set a user's password (admin action, no current-password check)."""
        user = await self.get_user(user_id)
        user.password = hash_password(password)
        await self.session.flush()
        return user

    async def delete_user(self, user_id: uuid.UUID) -> None:
        """Hard-delete a user (row removed)."""
        user = await self.get_user(user_id)
        await self.session.delete(user)
        await self.session.flush()

    async def _ensure_email_available(
        self, email: str, *, exclude_id: uuid.UUID | None = None
    ) -> None:
        stmt = select(User.id).where(User.email == email)
        if exclude_id is not None:
            stmt = stmt.where(User.id != exclude_id)
        if await self.session.scalar(stmt) is not None:
            raise ConflictException(
                f"User with email '{email}' already exists.", field="email"
            )
