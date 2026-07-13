from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List

from app.database import get_session
from app import models, schemas
from app.dependencies import get_current_user

router = APIRouter(prefix="/projects", tags=["projects"])


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

    return new_project


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
    return result.scalars().all()


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
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=403, detail="Not a member of this project")

    return project


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