# Day 25 - Async Python & Advanced FastAPI

## What I learned
- Sync vs async: async lets the server handle multiple requests concurrently instead of queueing them
- Converting FastAPI + SQLModel to async: asyncpg driver, AsyncSession, await on DB calls
- SQLModel's AsyncSession (not plain SQLAlchemy's) is needed for .exec() to work
- add() and add-like calls stay sync; get(), commit(), refresh(), delete() need await
- Lifespan handlers replace deprecated @app.on_event("startup")
- BackgroundTasks — run code after the response is sent (e.g. logging), without making the user wait
- Pagination via .offset()/.limit(), filtering via optional query params + .where()
- DATABASE_HOST=db only resolves inside Docker's network — learned this the hard way running uvicorn directly outside Docker
- response_model shapes what a route returns; list endpoints need list[Model], single-object endpoints need just Model
- API versioning via router prefix, added at the include_router() call in main.py (not inside the router itself) so the same router file stays reusable for future versions
- FastAPI auto-validates types (int, etc.) but doesn't enforce logical constraints (like "must be positive") unless you explicitly add them

## What I did
1. Copied Day24 app, converted database.py to async engine (asyncpg + SQLModel's AsyncSession)
2. Converted all 5 routes in tasks.py to async def, fixed main.py's lifespan handler
3. Converted conftest.py to async (aiosqlite, pytest-asyncio) — fixed 2 real bugs along the way (wrong AsyncSession import, missing await on delete())
4. Added BackgroundTasks to create_task — logs "Task created: {title}" after responding; verified via Docker Compose
5. Added pagination (skip/limit) to GET /tasks
6. Added optional completed filter to GET /tasks
7. Wrote tests proving pagination and filtering actually work
8. Added response_model to routes (Task, list[Task]) for cleaner output schemas
9. Added API versioning - moved all routes under /v1 prefix (in main.py, not tasks.py, to keep tasks.py version-agnostic)
10. Tested request validation edge cases:
    - skip=-5 -> accepted (200, empty list) - FastAPI doesn't reject negative ints by default (noted as a soft gap, not fixed today)
    - limit=abc -> rejected automatically by FastAPI's type validation (422)

## Results
- 18/18 tests passing
- 94% coverage (auth.py, models.py, tasks.py at 100%)
- Background task verified manually via docker exec + task_log.txt

## Known issues (not fixed today)
- database.py/main.py startup lines not fully covered — same reason as Day24 (test setup differs from real startup)
- httpx deprecation warning with TestClient — still not actionable

## Key commands
| Command | Purpose |
|---|---|
| pip install asyncpg sqlalchemy[asyncio] aiosqlite pytest-asyncio | Install async support |
| docker compose up --build | Test background task with real Postgres |
| docker exec -it <container> cat task_log.txt | Check background task's output inside container |
| pytest tests/ -v | Run all tests |