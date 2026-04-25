from fastapi import FastAPI

from app.api.routes import health, jobs, stats

app = FastAPI( title="URL Content Analyzer" )

app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
# app.include_router(stats.router, prefix="/stats", tags=["stats"])