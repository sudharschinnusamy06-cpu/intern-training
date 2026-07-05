from sqlmodel import create_engine, Session, SQLModel
from models import Task

DATABASE_URL = "postgresql://postgres:postgres123@localhost:5432/interndb"

engine = create_engine(DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)