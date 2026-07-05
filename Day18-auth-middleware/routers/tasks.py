from fastapi import APIRouter, HTTPException, Depends
from auth import verify_api_key
from sqlmodel import Session, select
from models import Task
from database import get_session

router = APIRouter()

@router.post("/tasks")
def create_task(task: Task, session: Session = Depends(get_session), auth: str = Depends(verify_api_key)):
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@router.get("/tasks")
def get_tasks(session: Session = Depends(get_session)):
    tasks = session.exec(select(Task)).all()
    return tasks

@router.get("/tasks/{task_id}")
def get_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: Task, session: Session = Depends(get_session), auth: str = Depends(verify_api_key)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.title = updated_task.title
    task.description = updated_task.description
    task.completed = updated_task.completed
    session.commit()
    session.refresh(task)
    return task

@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, session: Session = Depends(get_session), auth: str = Depends(verify_api_key)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    session.delete(task)
    session.commit()
    return {"message": "Task deleted"}