from app.models.job import Job


class JobRepository:
    async def create(self, session, url: str) -> Job:
        job = Job(
            url=url,
            status="pending",
            attempts=0,
        )
        session.add(job)
        await session.commit()
        await session.refresh(job)
        return job