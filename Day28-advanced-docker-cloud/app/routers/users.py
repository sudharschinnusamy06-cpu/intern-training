from fastapi import APIRouter, HTTPException, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from app.models import User
from app.database import get_session
from app.auth import hash_password, verify_password, create_access_token

router = APIRouter()


@router.post("/register")
async def register(username: str, password: str, session: AsyncSession = Depends(get_session)):
    hashed = hash_password(password)
    user = User(username=username, hashed_password=hashed)
    session.add(user)
    await session.commit()
    return {"message": "User created"}


@router.post("/login")
async def login(username: str, password: str, session: AsyncSession = Depends(get_session)):
    result = await session.exec(select(User).where(User.username == username))
    user = result.first()

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": username})
    return {"access_token": token}