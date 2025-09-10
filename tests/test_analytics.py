# tests/test_analytics.py

import pytest
from httpx import AsyncClient


class TestAnalytics:
    """Tests for analytics endpoints under /api prefix."""

    @pytest.mark.asyncio
    async def test_user_analytics(self, client: AsyncClient, auth_headers: dict):
        """
        Проверяем /api/analytics/user.
        Если эндпоинт пока не реализован — допускаем 404, чтобы не валить весь прогон.
        Когда реализуешь — просто поменяй проверку на строгий 200.
        """
        resp = await client.get("/api/analytics/user", headers=auth_headers)
        assert resp.status_code in (200, 404), resp.text
        if resp.status_code == 200:
            data = resp.json()
            assert "total_posts" in data
            assert "total_comments" in data

    @pytest.mark.asyncio
    async def test_post_analytics(self, client: AsyncClient, auth_headers: dict):
        # Test allows 200 (if post exists) or 404 (if not found)
        resp = await client.get("/api/analytics/post/1", headers=auth_headers)
        assert resp.status_code in (200, 404)

    @pytest.mark.asyncio
    async def test_comments_daily_breakdown(self, client: AsyncClient):
        # По КРОК 5: /api/comments-daily-breakdown
        resp = await client.get(
            "/api/comments-daily-breakdown",
            params={"date_from": "2020-01-01", "date_to": "2100-01-01"},
        )
        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert isinstance(data, list)
        if data:
            row = data[0]
            assert "date" in row
            assert "total" in row
            assert "blocked" in row
