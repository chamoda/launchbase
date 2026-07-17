import pytest
from faker import Faker

from app.models import User
from app.security import hash_password

fake = Faker()


@pytest.mark.asyncio
async def test_health_endpoint_healthy(async_client):
    """Test health endpoint returns healthy status when database is accessible."""
    response = await async_client.get("/platform/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


@pytest.mark.asyncio
async def test_auth_success(async_client):
    """Test successful authentication with valid credentials."""
    email = fake.email().lower()
    password = "testpassword123"

    # Create User directly for authentication testing
    async with getattr(async_client, "test_session_factory")() as db:
        user = User(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=email,
            password=hash_password(password),
            is_active=True,
        )
        db.add(user)
        await db.commit()

    # Test authentication
    auth_data = {"email": email, "password": password}
    response = await async_client.post("/platform/auth", json=auth_data)

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data


@pytest.mark.asyncio
async def test_auth_invalid_email(async_client):
    """Test authentication fails with non-existent email."""
    auth_data = {"email": "nonexistent@example.com", "password": "anypassword"}

    response = await async_client.post("/platform/auth", json=auth_data)

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_auth_invalid_password(async_client):
    """Test authentication fails with wrong password."""
    # Create a test user
    email = fake.email().lower()
    password = "correctpassword"

    async with getattr(async_client, "test_session_factory")() as db:
        user = User(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=email,
            password=hash_password(password),
            is_active=True,
        )
        db.add(user)
        await db.commit()

    # Test with wrong password
    auth_data = {"email": email, "password": "wrongpassword"}

    response = await async_client.post("/platform/auth", json=auth_data)

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_auth_missing_fields(async_client):
    """Test authentication fails with missing required fields."""
    auth_data = {
        "email": fake.email()
        # Missing password
    }

    response = await async_client.post("/platform/auth", json=auth_data)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_auth_invalid_email_format(async_client):
    """Test authentication fails with invalid email format."""
    auth_data = {"email": "invalid-email", "password": "somepassword"}

    response = await async_client.post("/platform/auth", json=auth_data)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_logout_success(async_client):
    """Test successful logout."""
    response = await async_client.post("/platform/logout")

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Successfully logged out"
