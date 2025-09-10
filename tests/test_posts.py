# tests/test_posts.py

import pytest
from httpx import AsyncClient


class TestPosts:
    """CRUD tests for posts."""

    @pytest.mark.asyncio
    async def test_create_post(self, client: AsyncClient, auth_headers: dict):
        # API creates post via /posts/ and returns 200 OK + content/is_blocked fields
        payload = {"content": "This is a test post."}

        resp = await client.post("/posts/", json=payload, headers=auth_headers)
        assert resp.status_code == 200, resp.text

        data = resp.json()
        assert "id" in data
        assert data["content"] == payload["content"]
        assert data.get("is_blocked") is False

    @pytest.mark.asyncio
    async def test_create_post_unauthorized(self, client: AsyncClient):
        payload = {"content": "Should fail"}
        resp = await client.post("/posts/", json=payload)
        assert resp.status_code == 401
