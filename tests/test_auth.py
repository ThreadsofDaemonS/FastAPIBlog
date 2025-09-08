import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestAuth:

    async def test_register_success(self, client: AsyncClient):
        """Test successful user registration."""
        user_data = {
            "email": "newuser@example.com",
            "password": "password123",
            "full_name": "New User"
        }
        response = await client.post("/auth/register", json=user_data)

        assert response.status_code == 200
        data = response.json()
        assert data["email"] == user_data["email"]
        assert data["full_name"] == user_data["full_name"]
        assert "id" in data
        assert "hashed_password" not in data

    async def test_register_duplicate_email(self, client: AsyncClient, test_user_data):
        """Test registration with duplicate email."""
        # Register first user
        await client.post("/auth/register", json=test_user_data)

        # Try to register same email again
        response = await client.post("/auth/register", json=test_user_data)

        assert response.status_code == 400
        assert "User already exists" in response.json()["detail"]

    async def test_login_success(self, client: AsyncClient, test_user_data):
        """Test successful login."""
        # Register user first
        await client.post("/auth/register", json=test_user_data)

        # Login
        login_data = {
            "username": test_user_data["email"],
            "password": test_user_data["password"]
        }
        response = await client.post("/auth/login", data=login_data)

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    async def test_login_invalid_credentials(self, client: AsyncClient, test_user_data):
        """Test login with invalid credentials."""
        # Register user first
        await client.post("/auth/register", json=test_user_data)

        # Try login with wrong password
        login_data = {
            "username": test_user_data["email"],
            "password": "wrongpassword"
        }
        response = await client.post("/auth/login", data=login_data)

        assert response.status_code == 401
        assert "Invalid credentials" in response.json()["detail"]

    async def test_login_nonexistent_user(self, client: AsyncClient):
        """Test login with non-existent user."""
        login_data = {
            "username": "nonexistent@example.com",
            "password": "password123"
        }
        response = await client.post("/auth/login", data=login_data)

        assert response.status_code == 401

    async def test_get_me_authenticated(self, client: AsyncClient, authenticated_user):
        """Test getting current user info when authenticated."""
        response = await client.get("/auth/me", headers=authenticated_user["headers"])

        assert response.status_code == 200
        data = response.json()
        assert data["email"] == authenticated_user["user_data"]["email"]

    async def test_get_me_unauthenticated(self, client: AsyncClient):
        """Test getting current user info without authentication."""
        response = await client.get("/auth/me")

        assert response.status_code == 401

    async def test_get_all_users(self, client: AsyncClient, authenticated_user):
        """Test getting all users list."""
        response = await client.get("/auth/all-users", headers=authenticated_user["headers"])

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1