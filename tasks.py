from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List
from app import database, schemas, models
from app.auth_utils import get_current_user
from app.logger import logger
from app.rate_limit import limiter


router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", response_model=schemas.TaskOut, status_code=201)
@limiter.limit("5/minute")
def create_task(request:Request,task: schemas.TaskCreate,
                db: Session = Depends(database.get_db),
                current_user: models.User = Depends(get_current_user)):
    """to create a new task with titile,description,owner_id and all"""

    db_task = models.Task(
        title=task.title,
        description=task.description,
        completed=task.completed,
        owner_id=current_user.id
    )
    print("Current user:", current_user)

    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    logger.info(f"Task created: '{db_task.title}' by user {current_user.id}")
    return db_task

@router.get("/", response_model=List[schemas.TaskOut])
@limiter.limit("5/minute")
def list_tasks(request:Request,db: Session = Depends(database.get_db),
               current_user: models.User = Depends(get_current_user)):
    """to get all task of the current user"""
    
    return db.query(models.Task).filter(models.Task.owner_id == current_user.id).order_by(models.Task.id.desc()).all()

@router.get("/{task_id}", response_model=schemas.TaskOut)
@limiter.limit("5/minute")
def get_task(request:Request,task_id: int,
             db: Session = Depends(database.get_db),
             current_user: models.User = Depends(get_current_user)):
    """to get the particular id task"""

    task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.owner_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=schemas.TaskOut)
@limiter.limit("5/minute")
def update_task(request:Request,task_id: int, payload: schemas.TaskUpdate,
                db: Session = Depends(database.get_db),
                current_user: models.User = Depends(get_current_user)):
    """to update the task with the mentioned task id"""
    task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.owner_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if payload.title is not None:
        task.title = payload.title
    if payload.description is not None:
        task.description = payload.description
    if payload.completed is not None:
        task.completed = payload.completed
    db.commit()
    db.refresh(task)
    logger.info(f"Task updated: '{task}' by user {current_user.id}")
    return task

@router.delete("/{task_id}", status_code=204)
@limiter.limit("5/minute")
def delete_task(request:Request,task_id: int,
                db: Session = Depends(database.get_db),
                current_user: models.User = Depends(get_current_user)):
    """helps to deleted the task mentioned """
    task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.owner_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    logger.info(f"Task deleted: '{task_id}'  deleted by user {current_user.id}")
    return None
