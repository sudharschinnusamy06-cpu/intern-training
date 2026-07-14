from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List, Optional
import json

from app.database import get_session
from app import models, schemas
from app.dependencies import get_current_user
from app.cache import redis_client

router = APIRouter(prefix="/projects/{project_id}/tasks", tags=["tasks"])


async def check_membership(project_id: int, user_id: int, session: AsyncSession):
    result = await session.execute(
        select(models.ProjectMember).where(
            models.ProjectMember.project_id == project_id,
            models.ProjectMember.user_id == user_id,
        )
    )
    if not result.scalars().first():
        raise HTTPException(status_code=403, detail="Not a member of this project")


@router.post("/", response_model=schemas.TaskRead)
async def create_task(
    project_id: int,
    task_in: schemas.TaskCreate,
    session: AsyncSession = Depends(get_session),
    current_user: models.User = Depends(get_current_user),
):
    await check_membership(project_id, current_user.id, session)

    new_task = models.Task(
        title=task_in.title,
        description=task_in.description,
        project_id=project_id,
        assigned_to=task_in.assigned_to,
    )
    session.add(new_task)
    await session.commit()
    await session.refresh(new_task)

    try:
        await redis_client.delete(f"tasks:{project_id}")
    except Exception:
        pass

    return new_task


@router.get("/", response_model=List[schemas.TaskRead])
async def list_tasks(
    project_id: int,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 10,
    session: AsyncSession = Depends(get_session),
    current_user: models.User = Depends(get_current_user),
):
    await check_membership(project_id, current_user.id, session)

    cache_key = f"tasks:{project_id}:{status}:{skip}:{limit}"

    try:
        cached = await redis_client.get(cache_key)
        if cached:
            return json.loads(cached)
    except Exception:
        pass

    query = select(models.Task).where(models.Task.project_id == project_id)
    if status:
        query = query.where(models.Task.status == status)
    query = query.offset(skip).limit(limit)

    result = await session.execute(query)
    tasks = result.scalars().all()

    try:
        await redis_client.setex(
            cache_key, 30, json.dumps([schemas.TaskRead.model_validate(t).model_dump(mode="json") for t in tasks])
        )
    except Exception:
        pass

    return tasks


@router.put("/{task_id}", response_model=schemas.TaskRead)
async def update_task(
    project_id: int,
    task_id: int,
    task_update: schemas.TaskUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: models.User = Depends(get_current_user),
):
    await check_membership(project_id, current_user.id, session)

    task = await session.get(models.Task, task_id)
    if not task or task.project_id != project_id:
        raise HTTPException(status_code=404, detail="Task not found")

    update_data = task_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    session.add(task)
    await session.commit()
    await session.refresh(task)

    try:
        await redis_client.delete(f"tasks:{project_id}")
    except Exception:
        pass

    return task


@router.delete("/{task_id}")
async def delete_task(
    project_id: int,
    task_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: models.User = Depends(get_current_user),
):
    await check_membership(project_id, current_user.id, session)

    task = await session.get(models.Task, task_id)
    if not task or task.project_id != project_id:
        raise HTTPException(status_code=404, detail="Task not found")

    await session.delete(task)
    await session.commit()

    return {"message": "Task deleted"}