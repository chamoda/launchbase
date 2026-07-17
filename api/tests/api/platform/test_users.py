import pytest
from faker import Faker

from app.models import User
from app.security import generate_jwt_token, hash_password

fake = Faker()


@pytest.mark.asyncio
async def test_users_me_success(async_client):
    """Test getting current user information with valid authentication."""
    # Create a test user
    email = fake.email().lower()
    password = "testpassword123"
    first_name = fake.first_name()
    last_name = fake.last_name()

    # Create User directly for authentication testing
    async with getattr(async_client, "test_session_factory")() as db:
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=hash_password(password),
            is_active=True,
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        user_id = user.id

    # Generate JWT token for authentication
    access_token = generate_jwt_token({"sub": str(user_id)})

    # Test getting user info with authentication
    async_client.cookies.set("access_token", f"Bearer {access_token}")
    response = await async_client.get("/platform/users/me")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(user_id)
    assert data["first_name"] == first_name
    assert data["last_name"] == last_name
    assert data["email"] == email
    assert "created_at" in data
    assert "updated_at" in data
    assert "password" not in data  # Password should not be exposed
    assert "is_active" not in data  # is_active not in response schema


@pytest.mark.asyncio
async def test_users_me_unauthorized(async_client):
    """Test getting current user information without authentication."""
    response = await async_client.get("/platform/users/me")

    assert response.status_code == 401
    data = response.json()
    assert "error" in data


@pytest.mark.asyncio
async def test_users_me_invalid_token(async_client):
    """Test getting current user information with invalid token."""
    async_client.cookies.set("access_token", "Bearer invalid_token")
    response = await async_client.get("/platform/users/me")

    assert response.status_code == 401
    data = response.json()
    assert "error" in data


@pytest.mark.asyncio
async def test_users_me_nonexistent_user(async_client):
    """Test getting current user information with token for non-existent user."""
    # Generate token for non-existent user
    fake_user_id = "550e8400-e29b-41d4-a716-446655440000"
    access_token = generate_jwt_token({"sub": fake_user_id})

    async_client.cookies.set("access_token", f"Bearer {access_token}")
    response = await async_client.get("/platform/users/me")

    assert response.status_code == 401
    data = response.json()
    assert "error" in data


@pytest.mark.asyncio
async def test_users_me_inactive_user(async_client):
    """Test getting current user information for inactive user."""
    # Note: The endpoint doesn't currently check is_active status
    # This test verifies current behavior - inactive users can still access their info
    email = fake.email().lower()
    password = "testpassword123"

    async with getattr(async_client, "test_session_factory")() as db:
        user = User(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=email,
            password=hash_password(password),
            is_active=False,  # Inactive user
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        user_id = user.id

    # Generate JWT token for inactive user
    access_token = generate_jwt_token({"sub": str(user_id)})

    async_client.cookies.set("access_token", f"Bearer {access_token}")
    response = await async_client.get("/platform/users/me")

    # Currently, the endpoint allows inactive users to access their info
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(user_id)
    assert data["email"] == email
