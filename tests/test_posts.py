import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestPosts:

    async def test_create_post_success(self, client: AsyncClient, authenticated_user):
        """Test successful post creation."""
        post_data = {
            "content": "This is a test post content",
            "auto_reply_enabled": True,
            "reply_delay_sec": 10
        }

        response = await client.post(
            "/posts/",
            json=post_data,
            headers=authenticated_user["headers"]
        )

        assert response.status_code == 200
        data = response.json()
        assert data["content"] == post_data["content"]
        assert data["auto_reply_enabled"] == post_data["auto_reply_enabled"]
        assert data["reply_delay_sec"] == post_data["reply_delay_sec"]
        assert data["is_blocked"] is False  # Should not be blocked initially
        assert "id" in data

    async def test_create_post_unauthenticated(self, client: AsyncClient):
        """Test post creation without authentication."""
        post_data = {
            "content": "This should fail",
            "auto_reply_enabled": False,
            "reply_delay_sec": 0
        }

        response = await client.post("/posts/", json=post_data)
        assert response.status_code == 401

    async def test_get_posts_list(self, client: AsyncClient, authenticated_user):
        """Test getting list of posts."""
        # Create a test post first
        post_data = {
            "content": "Test post for listing",
            "auto_reply_enabled": False,
            "reply_delay_sec": 0
        }
        await client.post(
            "/posts/",
            json=post_data,
            headers=authenticated_user["headers"]
        )

        # Get posts list
        response = await client.get("/posts/")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    async def test_get_post_by_id(self, client: AsyncClient, authenticated_user):
        """Test getting specific post by ID."""
        # Create a test post first
        post_data = {
            "content": "Test post for retrieval",
            "auto_reply_enabled": True,
            "reply_delay_sec": 5
        }
        create_response = await client.post(
            "/posts/",
            json=post_data,
            headers=authenticated_user["headers"]
        )
        post_id = create_response.json()["id"]

        # Get the post by ID
        response = await client.get(f"/posts/{post_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == post_id
        assert data["content"] == post_data["content"]

    async def test_get_nonexistent_post(self, client: AsyncClient):
        """Test getting non-existent post."""
        response = await client.get("/posts/99999")
        assert response.status_code == 404

    async def test_update_post_success(self, client: AsyncClient, authenticated_user):
        """Test successful post update."""
        # Create a test post first
        post_data = {
            "content": "Original content",
            "auto_reply_enabled": False,
            "reply_delay_sec": 0
        }
        create_response = await client.post(
            "/posts/",
            json=post_data,
            headers=authenticated_user["headers"]
        )
        post_id = create_response.json()["id"]

        # Update the post
        update_data = {
            "content": "Updated content",
            "auto_reply_enabled": True,
            "reply_delay_sec": 15
        }
        response = await client.put(
            f"/posts/{post_id}",
            json=update_data,
            headers=authenticated_user["headers"]
        )

        assert response.status_code == 200
        data = response.json()
        assert data["content"] == update_data["content"]
        assert data["auto_reply_enabled"] == update_data["auto_reply_enabled"]
        assert data["reply_delay_sec"] == update_data["reply_delay_sec"]

    async def test_delete_post_success(self, client: AsyncClient, authenticated_user):
        """Test successful post deletion."""
        # Create a test post first
        post_data = {
            "content": "Post to be deleted",
            "auto_reply_enabled": False,
            "reply_delay_sec": 0
        }
        create_response = await client.post(
            "/posts/",
            json=post_data,
            headers=authenticated_user["headers"]
        )
        post_id = create_response.json()["id"]

        # Delete the post
        response = await client.delete(
            f"/posts/{post_id}",
            headers=authenticated_user["headers"]
        )

        assert response.status_code == 200

        # Verify post is deleted
        get_response = await client.get(f"/posts/{post_id}")
        assert get_response.status_code == 404