import asyncio
import signal

from app.db.database import AsyncSessionLocal
from app.queue.redis_queue import RedisQueue
from app.services.job_processing_service import JobProcessingService

running = True

async def main():
    global running

    queue = RedisQueue()
    service = JobProcessingService()
    print("Worker started", flush=True)

    while running:
        job_id = await queue.pop()
        if job_id is None:
            continue
        if not running:
            break
        print(f"Received job: {job_id}", flush=True)
        async with AsyncSessionLocal() as session:
            await service.process_job(session, job_id)

    print("Worker shutting down gracefully...", flush=True)

def shutdown_handler(signum, frame):
    global running
    print("Shutdown signal received", flush=True)
    running = False


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, shutdown_handler)
    signal.signal(signal.SIGINT, shutdown_handler)

    asyncio.run(main())
