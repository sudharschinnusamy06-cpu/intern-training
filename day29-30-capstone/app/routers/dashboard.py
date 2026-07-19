from fastapi import APIRouter, Depends
from sqlmodel import select, func
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database import get_session
from app import models, schemas
from app.dependencies import get_current_user

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/stats", response_model=schemas.DashboardStats)
async def get_dashboard_stats(
    session: AsyncSession = Depends(get_session),
    current_user: models.User = Depends(get_current_user),
):
    # total projects the user is a member of
    total_projects_result = await session.execute(
        select(func.count(models.ProjectMember.id)).where(models.ProjectMember.user_id == current_user.id)
    )
    total_projects = total_projects_result.scalar_one()

    # project ids the user belongs to
    project_ids_result = await session.execute(
        select(models.ProjectMember.project_id).where(models.ProjectMember.user_id == current_user.id)
    )
    project_ids = project_ids_result.scalars().all()

    if not project_ids:
        return schemas.DashboardStats(
            total_projects=0, total_tasks=0, completed_tasks=0, pending_tasks=0
        )

    total_tasks_result = await session.execute(
        select(func.count(models.Task.id)).where(models.Task.project_id.in_(project_ids))
    )
    total_tasks = total_tasks_result.scalar_one()

    completed_result = await session.execute(
        select(func.count(models.Task.id)).where(
            models.Task.project_id.in_(project_ids), models.Task.status == "done"
        )
    )
    completed_tasks = completed_result.scalar_one()

    pending_tasks = total_tasks - completed_tasks

    return schemas.DashboardStats(
        total_projects=total_projects,
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        pending_tasks=pending_tasks,
    )