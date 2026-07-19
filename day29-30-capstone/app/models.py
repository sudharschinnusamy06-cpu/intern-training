from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship, UniqueConstraint


class User(SQLModel, table=True):
    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True)
    full_name: Optional[str] = None
    username: str = Field(nullable=False, unique=True)
    email: str = Field(unique=True)
    hashed_password: str
    role: str = Field(default="user")
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Project(SQLModel, table=True):
    __tablename__ = "projects"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    status: str = Field(default="active")
    owner_id: int = Field(foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ProjectMember(SQLModel, table=True):
    __tablename__ = "project_members"
    __table_args__ = (UniqueConstraint("project_id", "user_id", name="uq_project_user"),)

    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="projects.id")
    user_id: int = Field(foreign_key="users.id")


class Task(SQLModel, table=True):
    __tablename__ = "tasks"
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    status: str = Field(default="todo")
    priority: str = Field(default="medium")
    project_id: int = Field(foreign_key="projects.id", index=True)
    assigned_to: Optional[int] = Field(default=None, foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)