from fastapi import APIRouter, status
from sqlalchemy import text

from app.db.database import AsyncSessionLocal
from app.queue.redis_queue import RedisQueue

router = APIRouter()


@router.get("/")
async def health():
    db_status = "ok"
    redis_status = "ok"

    try:
        async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))
    except Exception as e:
        db_status = "error"

    try:
        queue = RedisQueue()
        await queue.ping()
    except Exception as e:
        redis_status = "error"

    overall_status = "ok" if db_status == "ok" and redis_status == "ok" else "error"

    return {
        "overall_status": overall_status,
        "db_status": db_status,
        "redis_status": redis_status,
    }