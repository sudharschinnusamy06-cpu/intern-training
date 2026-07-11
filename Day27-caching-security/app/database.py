from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from dotenv import load_dotenv
import os

load_dotenv()

password = os.getenv("DATABASE_PASSWORD")
host = os.getenv("DATABASE_HOST")

DATABASE_URL = f"postgresql+asyncpg://postgres:{password}@{host}:5432/interndb"

engine = create_async_engine(DATABASE_URL)


async def get_session():
    async with AsyncSession(engine) as session:
        yield session


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)