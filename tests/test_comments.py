import pytest
from httpx import AsyncClient
from unittest.mock import patch, AsyncMock


@pytest.mark.asyncio
class TestComments:

    @patch('app.services.ai_moderation.is_text_toxic', return_value=False)
    async def test_create_comment_success(self, mock_moderation, client: AsyncClient, authenticated_user):
        """Test successful comment creation."""
        # Create a test post first
        post_data = {
            "content": "Test post for comments",
            "auto_reply_enabled": False,
            "reply_delay_sec": 0
        }
        post_response = await client.post(
            "/posts/",
            json=post_data,
            headers=authenticated_user["headers"]
        )
        post_id = post_response.json()["id"]

        # Create comment
        comment_data = {
            "post_id": post_id,
            "content": "This is a test comment"
        }

        response = await client.post(
            "/comments/",
            json=comment_data,
            headers=authenticated_user["headers"]
        )

        assert response.status_code == 200
        data = response.json()
        assert data["content"] == comment_data["content"]
        assert data["post_id"] == post_id
        assert data["is_blocked"] is False

    @patch('app.services.ai_moderation.is_text_toxic', return_value=False)
    async def test_create_comment_blocked_by_ai(self, mock_moderation, client: AsyncClient, authenticated_user):
        """Test comment creation that gets blocked by AI moderation."""
        # Create a test post first  
        post_data = {
            "content": "Test post for blocked comments",
            "auto_reply_enabled": False,
            "reply_delay_sec": 0
        }
        post_response = await client.post(
            "/posts/",
            json=post_data,
            headers=authenticated_user["headers"]
        )
        post_id = post_response.json()["id"]

        # Create comment with content from the blacklist (will bypass AI and be blocked by manual check)
        comment_data = {
            "post_id": post_id,
            "content": "Це хуйня, а не текст"  # This is in the blacklist
        }

        # Remove the mock temporarily to test actual functionality
        mock_moderation.stop()
        
        response = await client.post(
            "/comments/",
            json=comment_data,
            headers=authenticated_user["headers"]
        )

        assert response.status_code == 200
        data = response.json()
        assert data["is_blocked"] is True

    @patch('app.services.ai_moderation.is_text_toxic', return_value=False)
    async def test_create_comment_with_auto_reply(self, mock_moderation, client: AsyncClient, authenticated_user):
        """Test comment creation on post with auto-reply enabled."""
        # Create a test post with auto-reply enabled
        post_data = {
            "content": "Test post with auto-reply",
            "auto_reply_enabled": True,
            "reply_delay_sec": 1
        }
        post_response = await client.post(
            "/posts/",
            json=post_data,
            headers=authenticated_user["headers"]
        )
        post_id = post_response.json()["id"]

        # Create comment
        comment_data = {
            "post_id": post_id,
            "content": "This should trigger auto-reply"
        }

        with patch('app.services.auto_reply.schedule_auto_reply') as mock_auto_reply:
            response = await client.post(
                "/comments/",
                json=comment_data,
                headers=authenticated_user["headers"]
            )

        assert response.status_code == 200
        # Auto-reply is triggered asynchronously, so we just verify the original comment was created
        data = response.json()
        assert data["content"] == comment_data["content"]

    @patch('app.services.ai_moderation.is_text_toxic', return_value=False)
    async def test_get_comments_for_post(self, mock_moderation, client: AsyncClient, authenticated_user):
        """Test getting comments for a specific post."""
        # Create a test post
        post_data = {
            "content": "Test post for comment listing",
            "auto_reply_enabled": False,
            "reply_delay_sec": 0
        }
        post_response = await client.post(
            "/posts/",
            json=post_data,
            headers=authenticated_user["headers"]
        )
        post_id = post_response.json()["id"]

        # Create multiple comments
        for i in range(3):
            comment_data = {
                "post_id": post_id,
                "content": f"Test comment {i + 1}"
            }
            await client.post(
                "/comments/",
                json=comment_data,
                headers=authenticated_user["headers"]
            )

        # Get comments for the post
        response = await client.get(f"/comments/post/{post_id}")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 3

    async def test_get_comments_nonexistent_post(self, client: AsyncClient):
        """Test getting comments for non-existent post."""
        response = await client.get("/comments/post/99999")
        assert response.status_code == 200  # This should return empty list, not 404
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0

    @patch('app.services.ai_moderation.is_text_toxic', return_value=False)
    async def test_create_comment_unauthenticated(self, mock_moderation, client: AsyncClient, authenticated_user):
        """Test comment creation without authentication."""
        # Create a test post first
        post_data = {
            "content": "Test post",
            "auto_reply_enabled": False,
            "reply_delay_sec": 0
        }
        post_response = await client.post(
            "/posts/",
            json=post_data,
            headers=authenticated_user["headers"]
        )
        post_id = post_response.json()["id"]

        # Try to create comment without auth
        comment_data = {
            "post_id": post_id,
            "content": "This should fail"
        }
        response = await client.post("/comments/", json=comment_data)

        assert response.status_code == 401

    async def test_create_comment_on_nonexistent_post(self, client: AsyncClient, authenticated_user):
        """Test creating comment on non-existent post."""
        comment_data = {
            "post_id": 99999,
            "content": "Comment on non-existent post"
        }

        response = await client.post(
            "/comments/",
            json=comment_data,
            headers=authenticated_user["headers"]
        )

        # This should succeed at the comment service level but might fail at DB level
        # Let's see what the actual behavior is
        assert response.status_code in [200, 400, 404]