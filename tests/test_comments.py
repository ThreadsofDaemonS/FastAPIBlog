import pytest
from httpx import AsyncClient
from unittest.mock import patch, AsyncMock


@pytest.mark.asyncio
class TestComments:

    async def test_create_comment_success(self, client: AsyncClient, authenticated_user):
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
            "content": "This is a test comment"
        }

        with patch('app.services.ai_moderation.moderate_comment') as mock_moderate:
            mock_moderate.return_value = {"is_blocked": False, "reason": None}

            response = await client.post(
                f"/comments/{post_id}",
                json=comment_data,
                headers=authenticated_user["headers"]
            )

        assert response.status_code == 200
        data = response.json()
        assert data["content"] == comment_data["content"]
        assert data["post_id"] == post_id
        assert data["is_blocked"] is False

    async def test_create_comment_blocked_by_ai(self, client: AsyncClient, authenticated_user):
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

        # Create comment with inappropriate content
        comment_data = {
            "content": "This is inappropriate content"
        }

        with patch('app.services.ai_moderation.moderate_comment') as mock_moderate:
            mock_moderate.return_value = {
                "is_blocked": True,
                "reason": "Inappropriate content detected"
            }

            response = await client.post(
                f"/comments/{post_id}",
                json=comment_data,
                headers=authenticated_user["headers"]
            )

        assert response.status_code == 200
        data = response.json()
        assert data["is_blocked"] is True

    async def test_create_comment_with_auto_reply(self, client: AsyncClient, authenticated_user):
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
            "content": "This should trigger auto-reply"
        }

        with patch('app.services.ai_moderation.moderate_comment') as mock_moderate, \
                patch('app.services.auto_reply.generate_auto_reply') as mock_auto_reply:
            mock_moderate.return_value = {"is_blocked": False, "reason": None}
            mock_auto_reply.return_value = "This is an auto-generated reply"

            response = await client.post(
                f"/comments/{post_id}",
                json=comment_data,
                headers=authenticated_user["headers"]
            )

        assert response.status_code == 200
        # Auto-reply is triggered asynchronously, so we just verify the original comment was created
        data = response.json()
        assert data["content"] == comment_data["content"]

    async def test_get_comments_for_post(self, client: AsyncClient, authenticated_user):
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
        with patch('app.services.ai_moderation.moderate_comment') as mock_moderate:
            mock_moderate.return_value = {"is_blocked": False, "reason": None}

            for i in range(3):
                comment_data = {"content": f"Test comment {i + 1}"}
                await client.post(
                    f"/comments/{post_id}",
                    json=comment_data,
                    headers=authenticated_user["headers"]
                )

        # Get comments for the post
        response = await client.get(f"/comments/{post_id}")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 3

    async def test_get_comments_nonexistent_post(self, client: AsyncClient):
        """Test getting comments for non-existent post."""
        response = await client.get("/comments/99999")
        assert response.status_code == 404

    async def test_create_comment_unauthenticated(self, client: AsyncClient, authenticated_user):
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
        comment_data = {"content": "This should fail"}
        response = await client.post(f"/comments/{post_id}", json=comment_data)

        assert response.status_code == 401

    async def test_create_comment_on_nonexistent_post(self, client: AsyncClient, authenticated_user):
        """Test creating comment on non-existent post."""
        comment_data = {"content": "Comment on non-existent post"}

        response = await client.post(
            "/comments/99999",
            json=comment_data,
            headers=authenticated_user["headers"]
        )

        assert response.status_code == 404