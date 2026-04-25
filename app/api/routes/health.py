from fastapi import APIRouter
from sqlalchemy import text

from app.db.database import AsyncSessionLocal

router = APIRouter()


@router.get("/")
async def health():
    try:
        async with AsyncSessionLocal() as db:
            await db.execute(text("SELECT 1"))
            return {
                "status": "ok",
                "database": "ok"
            }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }