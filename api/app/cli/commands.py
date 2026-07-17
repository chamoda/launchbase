import asyncio
import inspect
import secrets
from functools import partial, wraps

from pydantic import ValidationError
from sqlalchemy import select
from typer import BadParameter, Option, Typer

from app.cli.schemas import UserCreate
from app.database import AsyncSessionLocal, async_engine
from app.models import User
from app.security import hash_password


class AsyncTyper(Typer):
    @staticmethod
    def maybe_run_async(decorator, f):
        if inspect.iscoroutinefunction(f):

            @wraps(f)
            def runner(*args, **kwargs):
                # Close the shared session and dispose the engine's pool inside
                # the same event loop asyncio.run creates, so pooled asyncpg
                # connections are returned before the loop's greenlet is
                # finalized (otherwise the GC terminates them post-loop and
                # SQLAlchemy warns about non-checked-in connections).
                async def main():
                    try:
                        return await f(*args, **kwargs)
                    finally:
                        await session.close()
                        await async_engine.dispose()

                return asyncio.run(main())

            decorator(runner)
        else:
            decorator(f)
        return f

    def callback(self, *args, **kwargs):
        decorator = super().callback(*args, **kwargs)
        return partial(self.maybe_run_async, decorator)

    def command(self, *args, **kwargs):
        decorator = super().command(*args, **kwargs)
        return partial(self.maybe_run_async, decorator)


session = AsyncSessionLocal()
cli = AsyncTyper()


@cli.callback()
def main():
    """Launchbase management CLI."""
    # Present so Typer always runs in subcommand mode (`manage.py user-create`),
    # even while there is only a single command registered.


@cli.command()
async def create_user(
    first_name: str = Option(...),
    last_name: str = Option(...),
    email: str = Option(...),
    password: str = Option(None, help="Login password. Generated if not given."),
    admin: bool = Option(False, "--admin", help="Grant admin privileges."),
):
    """Create a user.

    The login password is generated unless provided with --password.
    Pass --admin to grant admin privileges.
    """
    try:
        data = UserCreate(first_name=first_name, last_name=last_name, email=email)
    except ValidationError as e:
        raise BadParameter("; ".join(err["msg"] for err in e.errors()))

    existing = (
        (await session.execute(select(User).where(User.email == data.email)))
        .scalars()
        .first()
    )
    if existing:
        raise BadParameter(f"User with email '{data.email}' already exists.")

    generated = password is None
    if generated:
        password = secrets.token_urlsafe(12)

    user = User(
        **data.model_dump(),
        password=hash_password(password),
        is_active=True,
        is_admin=admin,
    )
    session.add(user)
    await session.commit()
    print(f"{'Admin' if admin else 'User'} created: ", user.id)
    if generated:
        print("Generated password: ", password)
