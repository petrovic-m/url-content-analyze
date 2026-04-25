from app.models.job import Job
from app.queue.redis_queue import RedisQueue
from app.repositories.job_repository import JobRepository

class JobService:
    def __init__(self):
        self.job_repository = JobRepository()
        self.queue = RedisQueue()

    async def create_job(self, session, url: str) -> Job:
        job = await self.job_repository.create(session, url)
        await self.queue.push(job.id)
        return job