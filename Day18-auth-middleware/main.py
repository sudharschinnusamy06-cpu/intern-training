from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from routers import tasks
from database import create_db_and_tables
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    return response

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(tasks.router)