# URL Content Analyzer
A REST API service that accepts URLs for analysis, processes them asynchronously using workers, and provides results and statistics.

## Features:
* Submit URLs for analysis
* Asynchronous processing with Redis queue
* Worker-based architecture
* Retry with exponential backoff (up to 3 attempts)
* Per-domain rate limiting (max 2 concurrent requests)
* URL analysis:
    * HTTP status code
    * Response time
    * Page title
    * Word count
    * Top 10 words
* Health check (DB + Redis)
* Statistics endpoint
* Correlation ID for tracing requests
* Graceful shutdown support

## Architecture:
Client -> FastApi -> MySQL -> Redis (Queue) -> Worker -> HTTP requests (httpx) -> Processing -> MySQL update row

## Tech Stack as needed
* Python - FastAPI - library
    * SQLAchely
    * uvicorn[standard]==0.34.0
    * pydantic==2.10.4
    * pydantic-settings==2.7.1
    * sqlalchemy==2.0.36
    * aiomysql==0.2.0
    * cryptography==43.0.3 # without this, return a error: cryptography' package is required for sha256_password or caching_sha2_password auth methods
    * alembic==1.13.2
    * redis==5.0.4
    * httpx==0.27.0
    * beautifulsoup4==4.12.3
* MySQL
* Redis
* Docker

## API Endpoints

Create job:
POST /jobs

Body: 
``` 
{
  "url": "https://example.com"
}
```
Response: 
```
{
  "id": 1,
  "status": "pending",
  "attempts": 0,
  "correlation_id": "..."
}
```
Get job:
GET /jobs/{id}

Response: 
```
{
  "id": 1,
  "status": "pending",
  "attempts": 0,
  "correlation_id": "..."
}
```

List jobs:
GET /jobs?status=done&limit=10&offset=0

Get Stats:
GET /stats
```
{
  "by_status": {
    "done": 5,
    "failed": 2
  },
  "avg_response_time": 320,
  "jobs_per_minute": 1
}
```
Get Health:
GET /health

## Setup
1. Start a project: docker compose up --build
  - API is available at: http://localhost:8000
  - Swagger docs: http://localhost:8000/docs
2. Run migrations
  - ``docker compose exec api alembic upgrade head``
## Postman Collection
A Postman collection is included for easy API testing.

### How to use:
1. Open Postman
2. Click "Import"
3. Select the file:
   `URL Content Analyzer.postman_collection.json`
4. Run requests in the following order:
   - Create Job
   - Get Job
   - List Jobs
   - Stats
   - Health
