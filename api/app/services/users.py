import uuid
from typing import Any

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import (
    ConflictException,
    ResourceNotFoundException,
    ValidationException,
)
from app.models import User
from app.security import DUMMY_PASSWORD_HASH, hash_password, verify_password


class UserService:
    """Business logic for user records.

    Holds the DB session so callers pass it once and then issue user operations
    without threading the session through every call.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    def list_users_query(self) -> Select[tuple[User]]:
        """Return the query for listing users, newest first.

        Pagination is an HTTP concern, so the router pages this query (and
        counts the total) with fastapi-pagination rather than the service.
        """
        return select(User).order_by(User.created_at.desc(), User.id.desc())

    async def get_user(self, user_id: uuid.UUID) -> User:
        """Return a single user or raise 404."""
        result = await self.session.execute(select(User).where(User.id == user_id))
        user = result.scalars().first()
        if user is None:
            raise ResourceNotFoundException("User not found")
        return user

    async def authenticate(self, email: str, password: str) -> User | None:
        """Return the active user matching the credentials, or None.

        Unknown emails, wrong passwords and inactive accounts all return None so
        callers respond identically and account state isn't disclosed. A hash
        check always runs so timing doesn't reveal which emails exist.
        """
        user = await self.session.scalar(
            select(User).where(User.email == email.lower())
        )
        if user is None or user.password is None:
            verify_password(password, DUMMY_PASSWORD_HASH)
            return None
        if not verify_password(password, user.password) or not user.is_active:
            return None
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

    async def update_user(
        self,
        user_id: uuid.UUID,
        changes: dict[str, Any],
        *,
        actor_id: uuid.UUID | None = None,
    ) -> User:
        """Apply a partial (PATCH) update to a user.

        Only keys present in `changes` are touched. A null for any column is
        treated as "leave unchanged" so a non-nullable field is never blanked.
        Password is intentionally not updatable here — use `change_password`.
        `actor_id` is the acting admin; they can't revoke their own admin
        access or deactivate themselves, so an admin always remains.
        """
        changes.pop("password", None)
        user = await self.get_user(user_id)

        if user.id == actor_id:
            if changes.get("is_admin") is False:
                raise ValidationException(
                    "You can't remove your own admin access.", field="is_admin"
                )
            if changes.get("is_active") is False:
                raise ValidationException(
                    "You can't deactivate your own account.", field="is_active"
                )

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
        """Set a user's password (admin action, no current-password check).

        Bumps `token_version` so every session issued with the old password is
        signed out.
        """
        user = await self.get_user(user_id)
        user.password = hash_password(password)
        user.token_version += 1
        await self.session.flush()
        return user

    async def delete_user(
        self, user_id: uuid.UUID, *, actor_id: uuid.UUID | None = None
    ) -> None:
        """Hard-delete a user (row removed). `actor_id` can't delete themselves."""
        if user_id == actor_id:
            raise ValidationException("You can't delete your own account.")
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
