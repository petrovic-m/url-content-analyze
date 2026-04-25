import redis.asyncio as redis
import os

REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')
class RedisQueue:
    def __init__(self):
        self.connection = redis.from_url(REDIS_URL)

    async def ping(self) -> bool:
        return await self.connection.ping()

    async def push(self, job_id:int):
        await self.connection.lpush("jobs_queue", job_id)

    async def pop(self):
        result = await self.connection.brpop("jobs_queue", timeout=1)
        if(result):
            _, job_id = result
            return int(job_id)
        return None