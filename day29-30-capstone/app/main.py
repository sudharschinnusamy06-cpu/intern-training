from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.database import init_db
from app.routers import auth, projects  # tasks import added later on Day 30
from app.rate_limiter import limiter
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(title="Employee/Project Management API", lifespan=lifespan)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(auth.router)
app.include_router(projects.router)
# app.include_router(tasks.router)  # will add on Day 30


@app.get("/")
def root():
    return {"message": "Employee/Project Management API is running"}