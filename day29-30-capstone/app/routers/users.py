from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select, func
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List

from app.database import get_session
from app import models, schemas
from app.dependencies import get_current_user
from app.auth import hash_password, verify_password

router = APIRouter(prefix="/users", tags=["users"])


async def _project_count(user_id: int, session: AsyncSession) -> int:
    result = await session.execute(
        select(func.count(models.ProjectMember.id)).where(models.ProjectMember.user_id == user_id)
    )
    return result.scalar_one()


@router.get("/me", response_model=schemas.UserRead)
async def get_my_profile(current_user: models.User = Depends(get_current_user)):
    return current_user


@router.put("/me", response_model=schemas.UserRead)
async def update_my_profile(
    update_in: schemas.UserUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: models.User = Depends(get_current_user),
):
    update_data = update_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(current_user, field, value)

    session.add(current_user)
    await session.commit()
    await session.refresh(current_user)
    return current_user


@router.put("/me/password")
async def change_password(
    password_in: schemas.PasswordChange,
    session: AsyncSession = Depends(get_session),
    current_user: models.User = Depends(get_current_user),
):
    if not verify_password(password_in.current_password, current_user.hashed_password):
        raise HTTPException(status_code=401, detail="Current password is incorrect")

    current_user.hashed_password = hash_password(password_in.new_password)
    session.add(current_user)
    await session.commit()
    return {"message": "Password updated successfully"}


@router.get("/", response_model=List[dict])
async def list_users(
    session: AsyncSession = Depends(get_session),
    current_user: models.User = Depends(get_current_user),
):
    result = await session.execute(select(models.User))
    users = result.scalars().all()

    output = []
    for u in users:
        count = await _project_count(u.id, session)
        output.append({
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "role": u.role,
            "project_count": count,
            "created_at": u.created_at,
        })
    return output

@router.put("/{user_id}/role")
async def update_user_role(
    user_id: int,
    role: str,
    session: AsyncSession = Depends(get_session),
    current_user: models.User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can change roles")

    if role not in ("user", "manager", "admin"):
        raise HTTPException(status_code=400, detail="Invalid role")

    target_user = await session.get(models.User, user_id)
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")

    target_user.role = role
    session.add(target_user)
    await session.commit()
    return {"message": f"Role updated to {role}"}