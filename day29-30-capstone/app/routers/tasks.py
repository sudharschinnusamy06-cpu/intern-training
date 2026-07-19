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


async def _to_task_read(task: models.Task, session: AsyncSession) -> schemas.TaskRead:
    assigned_username = None
    if task.assigned_to:
        assigned_user = await session.get(models.User, task.assigned_to)
        assigned_username = assigned_user.username if assigned_user else None

    return schemas.TaskRead(
        id=task.id,
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority,
        project_id=task.project_id,
        assigned_to=task.assigned_to,
        assigned_username=assigned_username,
        created_at=task.created_at,
    )


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
        priority=task_in.priority or "medium",
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

    return await _to_task_read(new_task, session)


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

    task_reads = [await _to_task_read(t, session) for t in tasks]

    try:
        await redis_client.setex(
            cache_key, 30, json.dumps([t.model_dump(mode="json") for t in task_reads])
        )
    except Exception:
        pass

    return task_reads


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

    return await _to_task_read(task, session)


@router.delete("/{task_id}")
async def delete_task(
    project_id: int,
    task_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: models.User = Depends(get_current_user),
):
    await check_membership(project_id, current_user.id, session)

    if current_user.role not in ("admin", "manager"):
        raise HTTPException(status_code=403, detail="Only admin/manager can delete tasks")

    task = await session.get(models.Task, task_id)
    if not task or task.project_id != project_id:
        raise HTTPException(status_code=404, detail="Task not found")

    await session.delete(task)
    await session.commit()

    return {"message": "Task deleted"}