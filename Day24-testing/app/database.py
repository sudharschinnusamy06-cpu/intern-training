from sqlmodel import create_engine, Session, SQLModel
from dotenv import load_dotenv
import os

load_dotenv()

password = os.getenv("DATABASE_PASSWORD")
host = os.getenv("DATABASE_HOST")

DATABASE_URL = f"postgresql://postgres:{password}@{host}:5432/interndb"

engine = create_engine(DATABASE_URL)


def get_session():
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
