from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, EmailStr


# ---------- User ----------
class UserCreate(BaseModel):
    full_name: str
    username: str
    email: EmailStr
    password: str


class UserRead(BaseModel):
    id: int
    full_name: Optional[str]
    username: str
    email: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None


class PasswordChange(BaseModel):
    current_password: str
    new_password: str


# ---------- Auth ----------
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ---------- Project ----------
class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None


class ProjectRead(BaseModel):
    id: int
    name: str
    description: Optional[str]
    status: str
    owner_id: int
    owner_username: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


# ---------- Task ----------
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Optional[str] = "medium"
    assigned_to: Optional[int] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    assigned_to: Optional[int] = None


class TaskRead(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str
    priority: str
    project_id: int
    assigned_to: Optional[int]
    assigned_username: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


# ---------- Dashboard ----------
class DashboardStats(BaseModel):
    total_projects: int
    total_tasks: int
    completed_tasks: int
    pending_tasks: int