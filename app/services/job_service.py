from app.models.job import Job
from app.queue.redis_queue import RedisQueue
from app.repositories.job_repository import JobRepository
from typing import List

class JobService:
    def __init__(self):
        self.job_repository = JobRepository()
        self.queue = RedisQueue()

    async def create_job(self, session, url: str, correlation_id: str) -> Job:
        job = await self.job_repository.create(session, url, correlation_id)
        await self.queue.push(job.id)
        return job

    async def get_job(self, session, job_id: int) -> Job:
        return await self.job_repository.find_by_id(session, job_id)

    async def list_jobs(self, session, status: str | None, limit: int, offset: int) -> List[Job]:
        return await self.job_repository.list_jobs(session, status, limit, offset)

    async def get_stats(self, session):
        return await self.job_repository.get_stats(session)