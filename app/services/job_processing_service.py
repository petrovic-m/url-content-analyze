from app.queue.redis_queue import RedisQueue
from app.repositories.job_repository import JobRepository
from app.services.analyzer_service import AnalyzerService
import asyncio

class JobProcessingService:
    def __init__(self):
        self.job_repository = JobRepository()
        self.analyzer_service = AnalyzerService()
        self.queue = RedisQueue()

    async def process_job(self, session, job_id: int):
        job = await self.job_repository.find_by_id(session, job_id)
        if not job:
            print(f"Job not found: {job_id}", flush=True)
            return
        try:
            job = await self.job_repository.change_process(session, job)
            result = await self.analyzer_service.analyze(job.url)
            job = await self.job_repository.mark_done(session, job, result)
            print(
                {
                    "event": "job_processing_done",
                    "job_id": job.id,
                    "correlation_id": job.correlation_id,
                    "status": job.status,
                },
                flush=True,
            )
        except Exception as e:
            err_msg = repr(e)
            job = await self.job_repository.increment_attempts(session, job)
            if job.attempts < 3:
                print(
                    {
                        "event": "job_processing_failed",
                        "job_id": job.id,
                        "correlation_id": job.correlation_id,
                        "error": err_msg,
                        "attempts": job.attempts,
                    },
                    flush=True,
                )
                await asyncio.sleep(2 ** job.attempts)
                job.status = "pending"
                await session.commit()
                await self.queue.push(job.id)
            else:
                job = await self.job_repository.mark_failed(session, job, err_msg)
                print(f"Job {job.id} permanently failed: {err_msg}", flush=True)