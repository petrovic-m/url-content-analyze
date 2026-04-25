from uuid import uuid4
from fastapi import APIRouter, HTTPException, Request

from app.db.database import AsyncSessionLocal
from app.schemas.job import JobCreateRequest
from app.services.job_service import JobService
router = APIRouter()
service = JobService()
@router.post("/")
async def create_jobs(payload: JobCreateRequest, request: Request):
    correlation_id = request.headers.get("X-Correlation-ID", str(uuid4()))
    async with AsyncSessionLocal() as session:
        job = await service.create_job(session, str(payload.url), correlation_id)
        return {
            "id": job.id,
            "status": job.status,
            "attempts": job.attempts,
            "correlation_id": correlation_id
        }

@router.get("/")
async def list_jobs(status: str | None = None, limit: int = 10, offset: int = 0):
    async with AsyncSessionLocal() as session:
        jobs = await service.list_jobs(session, status, limit, offset)
        return [
            {
                "id": job.id,
                "url": job.url,
                "status": job.status,
                "attempts": job.attempts,
                "http_status_code": job.http_status_code,
                "response_time_ms": job.response_time_ms,
                "title": job.title,
                "word_count": job.word_count,
                "top_words": job.top_words,
                "error_message": job.error_message,
            }
            for job in jobs
        ]

@router.get("/{job_id}")
async def get_jobs(job_id: int):
    async with AsyncSessionLocal() as session:
        job = await service.get_job(session, int(job_id))
        if job is None:
            raise HTTPException(status_code=404, detail="Job not found")
        return {
            "id": job.id,
            "url": job.url,
            "status": job.status,
            "attempts": job.attempts,
            "http_status_code": job.http_status_code,
            "response_time_ms": job.response_time_ms,
            "title": job.title,
            "word_count": job.word_count,
            "top_words": job.top_words,
            "error_message": job.error_message,
        }