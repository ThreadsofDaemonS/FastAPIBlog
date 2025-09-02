from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from datetime import date

from app.core.db import get_db

router = APIRouter()

@router.get("/comments-daily-breakdown")
async def comments_daily_breakdown(
    date_from: date = Query(..., description="Початкова дата (YYYY-MM-DD)"),
    date_to: date = Query(..., description="Кінцева дата (YYYY-MM-DD)"),
    db: AsyncSession = Depends(get_db)
) -> list[dict]:
    stmt = text("""
        SELECT
            DATE(created_at) AS day,
            COUNT(*) AS total_comments,
            SUM(CASE WHEN is_blocked THEN 1 ELSE 0 END) AS blocked_comments
        FROM comments
        WHERE created_at BETWEEN :date_from AND :date_to
        GROUP BY day
        ORDER BY day
    """)
    result = await db.execute(stmt, {"date_from": date_from, "date_to": date_to})
    rows = result.fetchall()
    return [
        {
            "date": str(row.day),
            "total_comments": row.total_comments,
            "blocked_comments": row.blocked_comments or 0
        }
        for row in rows
    ]