from ast import List
from statistics import correlation

from app.models import job
from app.models.job import Job
from typing import List
from sqlalchemy import select, func
from datetime import datetime, timedelta, UTC

class JobRepository:
    async def create(self, session, url: str, correlation_id: str) -> Job:
        job = Job(
            correlation_id=correlation_id,
            url=url,
            status="pending",
            attempts=0,
        )
        session.add(job)
        await session.commit()
        await session.refresh(job)
        return job

    async def find_by_id(self, session, job_id: int) -> Job:
        return await session.get(Job, job_id)

    async def change_process(self, session, job: Job) -> Job:
        job.status = "processing"
        await session.commit()
        await session.refresh(job)
        return job

    async def mark_done(self, session, job: Job, result: dict) -> Job:
        job.status = "done"
        job.http_status_code = result["http_status_code"]
        job.rest_status_code = result["response_time_ms"]
        job.title = result["title"]
        job.word_count = result["word_count"]
        job.top_words = result["top_words"]
        await session.commit()
        await session.refresh(job)
        return job

    async def mark_failed(self, session, job: Job, err_msg: str) -> Job:
        job.status = "failed"
        job.error_message = err_msg
        await session.commit()
        await session.refresh(job)
        return job

    async def increment_attempts(self, session, job: Job) -> Job:
        job.attempts += 1
        await session.commit()
        await session.refresh(job)
        return job

    async def list_jobs(self, session, status: str | None, limit: int, offset: int) -> List[Job]:
        query = select(Job).order_by(Job.id.desc()).limit(limit).offset(offset)

        if status:
            query = query.where(Job.status == status)

        result = await session.execute(query)
        return result.scalars().all()

    async def get_stats(self, session):
        status_result = await session.execute(
            select(
                Job.status,
                func.count(Job.id)
            ).group_by(Job.status)
        )
        avg_result = await session.execute(
            select(func.avg(Job.response_time_ms))
            .where(Job.response_time_ms.is_not(None))
        )
        one_minute_ago = datetime.now(UTC) - timedelta(minutes=1)
        jobs_per_minute_result = await session.execute(
            select(func.count(Job.id))
            .where(Job.created_at >= one_minute_ago)
        )

        by_status = {
            status: count
            for status, count in status_result.all()
        }
        avg_response_time = avg_result.scalar()
        jobs_per_minute = jobs_per_minute_result.scalar()
        return {
            "by_status": by_status,
            "avg_response_time": int(avg_response_time) if avg_response_time is not None else 0,
            "jobs_per_minute": jobs_per_minute or 0,
        }