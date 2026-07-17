#!/bin/env python

import asyncio
import inspect
from functools import partial, wraps

from typer import Typer

from app.database import AsyncSessionLocal
from app.models import User
from app.security import hash_password


class AsyncTyper(Typer):
    @staticmethod
    def maybe_run_async(decorator, f):
        if inspect.iscoroutinefunction(f):

            @wraps(f)
            def runner(*args, **kwargs):
                return asyncio.run(f(*args, **kwargs))

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


@cli.command()
async def create_user(
    first_name: str,
    last_name: str,
    email: str,
    password: str,
):
    user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=hash_password(password),
        is_active=True,
    )
    session.add(user)
    await session.commit()
    print("User created: ", user.id)


if __name__ == "__main__":
    cli()
