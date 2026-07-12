import json
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks, Request
from sqlmodel import select
from typing import Optional
from sqlmodel.ext.asyncio.session import AsyncSession

from app.auth import get_current_user
from app.models import Task
from app.database import get_session
from app.redis_client import redis_client
from app.rate_limiter import limiter
from fastapi import UploadFile, File
from app.s3_utils import upload_file_to_s3

router = APIRouter()


def log_task_creation(title: str):
    with open("task_log.txt", "a") as f:
        f.write(f"Task created: {title}\n")


@router.post("/tasks", response_model=Task)
async def create_task(
    task: Task,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_session),
    current_user: str = Depends(get_current_user),
):
    session.add(task)
    await session.commit()
    await session.refresh(task)

    background_tasks.add_task(log_task_creation, task.title)

    return task


@router.get("/tasks", response_model=list[Task])
@limiter.limit("5/minute")
async def get_tasks(
    request: Request,
    skip: int = 0,
    limit: int = 10,
    completed: Optional[bool] = None,
    session: AsyncSession = Depends(get_session),
):
    cache_key = f"tasks:{skip}:{limit}:{completed}"

    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)

    query = select(Task)

    if completed is not None:
        query = query.where(Task.completed == completed)

    result = await session.exec(query.offset(skip).limit(limit))
    tasks = result.all()

    redis_client.set(cache_key, json.dumps([task.model_dump() for task in tasks]), ex=30)

    return tasks


@router.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int, session: AsyncSession = Depends(get_session)):
    task = await session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/tasks/{task_id}", response_model=Task)
async def update_task(
    task_id: int,
    updated_task: Task,
    session: AsyncSession = Depends(get_session),
    current_user: str = Depends(get_current_user),
):
    task = await session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.title = updated_task.title
    task.description = updated_task.description
    task.completed = updated_task.completed
    await session.commit()
    await session.refresh(task)
    return task


@router.delete("/tasks/{task_id}")
async def delete_task(
    task_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: str = Depends(get_current_user),
):
    task = await session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    await session.delete(task)
    await session.commit()
    return {"message": "Task deleted"}

@router.post("/tasks/{task_id}/upload")
async def upload_task_file(
    task_id: int,
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_session),
    current_user: str = Depends(get_current_user),
):
    task = await session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    key = f"tasks/{task_id}/{file.filename}"

    url = await upload_file_to_s3(file, key)

    return {"filename": file.filename, "url": url}