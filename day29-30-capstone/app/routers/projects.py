from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List

from app.database import get_session
from app import models, schemas
from app.dependencies import get_current_user

router = APIRouter(prefix="/projects", tags=["projects"])


async def _to_project_read(project: models.Project, session: AsyncSession) -> schemas.ProjectRead:
    owner = await session.get(models.User, project.owner_id)
    return schemas.ProjectRead(
        id=project.id,
        name=project.name,
        description=project.description,
        status=project.status,
        owner_id=project.owner_id,
        owner_username=owner.username if owner else None,
        created_at=project.created_at,
    )


@router.post("/", response_model=schemas.ProjectRead)
async def create_project(
    project_in: schemas.ProjectCreate,
    session: AsyncSession = Depends(get_session),
    current_user: models.User = Depends(get_current_user),
):
    new_project = models.Project(
        name=project_in.name,
        description=project_in.description,
        owner_id=current_user.id,
    )
    session.add(new_project)
    await session.commit()
    await session.refresh(new_project)

    membership = models.ProjectMember(project_id=new_project.id, user_id=current_user.id)
    session.add(membership)
    await session.commit()

    return await _to_project_read(new_project, session)


@router.get("/", response_model=List[schemas.ProjectRead])
async def list_my_projects(
    session: AsyncSession = Depends(get_session),
    current_user: models.User = Depends(get_current_user),
):
    result = await session.execute(
        select(models.Project)
        .join(models.ProjectMember, models.ProjectMember.project_id == models.Project.id)
        .where(models.ProjectMember.user_id == current_user.id)
    )
    projects = result.scalars().all()
    return [await _to_project_read(p, session) for p in projects]


@router.get("/{project_id}", response_model=schemas.ProjectRead)
async def get_project(
    project_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: models.User = Depends(get_current_user),
):
    project = await session.get(models.Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    result = await session.execute(
        select(models.ProjectMember).where(
            models.ProjectMember.project_id == project_id,
            models.ProjectMember.user_id == current_user.id,
        )
    )
    if not result.scalars().first():
        raise HTTPException(status_code=403, detail="Not a member of this project")

    return await _to_project_read(project, session)


@router.post("/{project_id}/members")
async def add_member(
    project_id: int,
    user_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: models.User = Depends(get_current_user),
):
    project = await session.get(models.Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only the owner can add members")

    membership = models.ProjectMember(project_id=project_id, user_id=user_id)
    session.add(membership)
    await session.commit()
    return {"message": "Member added"}

@router.put("/{project_id}", response_model=schemas.ProjectRead)
async def update_project(
    project_id: int,
    project_update: schemas.ProjectUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: models.User = Depends(get_current_user),
):
    project = await session.get(models.Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    update_data = project_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(project, field, value)

    session.add(project)
    await session.commit()
    await session.refresh(project)
    return await _to_project_read(project, session)


@router.delete("/{project_id}")
async def delete_project(
    project_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: models.User = Depends(get_current_user),
):
    project = await session.get(models.Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only the owner can delete this project")

    await session.delete(project)
    await session.commit()
    return {"message": "Project deleted"}