import asyncio
import logging
import warnings

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from testcontainers.postgres import PostgresContainer

from app.database import Base, get_db

# Suppress SQLAlchemy pool connection errors during test cleanup
logging.getLogger("sqlalchemy.pool.impl.AsyncAdaptedQueuePool").setLevel(
    logging.CRITICAL
)

# Filter out the specific async warning that occurs during testing
# This is a known issue with async SQLAlchemy connections in tests
warnings.filterwarnings(
    "ignore",
    message="coroutine.*was never awaited",
    category=RuntimeWarning,
    module=".*",
)

# Filter out connection cleanup warnings during test teardown
warnings.filterwarnings(
    "ignore",
    message=".*Event loop is closed.*",
    category=RuntimeWarning,
    module=".*",
)

# Filter out SQLAlchemy pool cleanup errors during testing
warnings.filterwarnings(
    "ignore",
    message=".*Exception terminating connection.*",
    category=Warning,
    module=".*",
)

# Suppress asyncpg connection closure warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module="asyncpg.*")


@pytest.fixture(scope="session")
def postgres_container():
    """Start PostgreSQL container for tests."""
    with PostgresContainer("postgres:16") as postgres:
        yield postgres


@pytest.fixture
async def async_client(postgres_container):
    """Create async test client with test database."""
    # Create engine for each test to avoid event loop issues
    db_url = postgres_container.get_connection_url().replace("psycopg2", "asyncpg")
    engine = create_async_engine(
        db_url,
        echo=False,
        pool_pre_ping=False,  # Disable pre-ping to avoid cleanup issues
        pool_recycle=300,
        pool_timeout=10,
        pool_size=2,  # Smaller pool for tests
        max_overflow=5,
        connect_args={"server_settings": {"application_name": "pytest"}},
    )

    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Create session factory
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    async def get_test_db():
        async with session_factory() as session:
            yield session

    # Override the database dependency
    from app.main import app as fastapi_app

    fastapi_app.dependency_overrides[get_db] = get_test_db

    # Also override the database engine at the module level to prevent conflicts
    import app.database

    original_engine = app.database.async_engine
    original_session_local = app.database.AsyncSessionLocal

    app.database.async_engine = engine
    app.database.AsyncSessionLocal = session_factory

    # Store the session factory for direct use in tests
    test_session_factory = session_factory

    async with AsyncClient(
        transport=ASGITransport(app=fastapi_app), base_url="http://localhost"
    ) as ac:
        # Attach the session factory to the client for direct database access
        # Using setattr to avoid type checking issues
        setattr(ac, "test_session_factory", test_session_factory)
        yield ac

    # Cleanup - ensure proper order and error handling
    fastapi_app.dependency_overrides.clear()

    # Restore original database setup
    app.database.async_engine = original_engine
    app.database.AsyncSessionLocal = original_session_local

    # Graceful engine disposal with error handling
    try:
        # Use a shorter timeout and handle cleanup gracefully
        await asyncio.wait_for(engine.dispose(), timeout=2.0)
    except asyncio.TimeoutError:
        # If disposal times out, the connections will be forcefully closed
        pass
    except Exception:
        # Ignore other disposal errors during test cleanup
        pass
