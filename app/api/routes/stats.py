from fastapi import APIRouter, HTTPException
from app.db.database import AsyncSessionLocal
from app.services.job_service import JobService

router = APIRouter()
service = JobService()

@router.get("/")
async def get_stats():
    async with AsyncSessionLocal() as session:
        return await service.get_stats(session)