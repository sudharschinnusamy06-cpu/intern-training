from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from sqlmodel import select
from typing import Optional
from sqlmodel.ext.asyncio.session import AsyncSession

from app.auth import verify_api_key
from app.models import Task
from app.database import get_session

router = APIRouter()


def log_task_creation(title: str):
    with open("task_log.txt", "a") as f:
        f.write(f"Task created: {title}\n")


@router.post("/tasks", response_model=Task)
async def create_task(
    task: Task,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_session),
    auth: str = Depends(verify_api_key),
):
    session.add(task)
    await session.commit()
    await session.refresh(task)

    background_tasks.add_task(log_task_creation, task.title)

    return task


@router.get("/tasks", response_model=list[Task])
async def get_tasks(
    skip: int = 0,
    limit: int = 10,
    completed: Optional[bool] = None,
    session: AsyncSession = Depends(get_session),
):
    query = select(Task)

    if completed is not None:
        query = query.where(Task.completed == completed)

    result = await session.exec(query.offset(skip).limit(limit))
    tasks = result.all()
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
    auth: str = Depends(verify_api_key),
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
    auth: str = Depends(verify_api_key),
):
    task = await session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    await session.delete(task)
    await session.commit()
    return {"message": "Task deleted"}