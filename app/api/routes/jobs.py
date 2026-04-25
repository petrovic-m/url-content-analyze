from fastapi import APIRouter

from app.db.database import AsyncSessionLocal
from app.schemas.job import JobCreateRequest
from app.services.job_service import JobService
router = APIRouter()
service = JobService()
@router.post("/")
async def create_jobs(payload: JobCreateRequest):
    async with AsyncSessionLocal() as session:
        job = await service.create_job(session, str(payload.url))
        return {
            "id": job.id,
            "status": job.status,
            "attempts": job.attempts
        }

@router.get("/")
async def list_jobs():
    return {"message": "Hello World"}

@router.get("/{job_id}")
async def get_jobs(job_id: int):
    return {"message": "Hello World"}