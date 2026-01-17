from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.database import get_db
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskStatistics
from app.models.task import Task
from app.models.user import User
from app.middleware.auth import get_current_user

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new task"""
    new_task = Task(
        title=task_data.title,
        description=task_data.description,
        status=task_data.status,
        priority=task_data.priority,
        due_date=task_data.due_date,
        created_by=current_user.id,
        assigned_to=task_data.assigned_to
    )
    
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    
    return new_task


@router.get("/", response_model=List[TaskResponse])
def get_all_tasks(
    status: Optional[str] = Query(None, regex="^(pending|in_progress|completed)$"),
    priority: Optional[str] = Query(None, regex="^(low|medium|high)$"),
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all tasks with optional filters"""
    query = db.query(Task)
    
    # Authorization: users see own tasks, admins see all
    if current_user.role != "admin":
        query = query.filter(
            (Task.created_by == current_user.id) | (Task.assigned_to == current_user.id)
        )
    
    # Apply filters
    if status:
        query = query.filter(Task.status == status)
    
    if priority:
        query = query.filter(Task.priority == priority)
    
    if search:
        query = query.filter(Task.title.ilike(f"%{search}%"))
    
    tasks = query.all()
    return tasks


@router.get("/statistics", response_model=TaskStatistics)
def get_task_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get task statistics"""
    query = db.query(Task)
    
    # Filter by user if not admin
    if current_user.role != "admin":
        query = query.filter(
            (Task.created_by == current_user.id) | (Task.assigned_to == current_user.id)
        )
    
    total_tasks = query.count()
    completed_tasks = query.filter(Task.status == "completed").count()
    pending_tasks = query.filter(Task.status == "pending").count()
    in_progress_tasks = query.filter(Task.status == "in_progress").count()
    high_priority = query.filter(Task.priority == "high").count()
    medium_priority = query.filter(Task.priority == "medium").count()
    low_priority = query.filter(Task.priority == "low").count()
    
    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "in_progress_tasks": in_progress_tasks,
        "high_priority": high_priority,
        "medium_priority": medium_priority,
        "low_priority": low_priority
    }


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a single task by ID"""
    task = db.query(Task).filter(Task.id == task_id).first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # Authorization: creator, assignee, or admin only
    if (current_user.role != "admin" and 
        task.created_by != current_user.id and 
        task.assigned_to != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this task"
        )
    
    return task


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a task"""
    task = db.query(Task).filter(Task.id == task_id).first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # Authorization logic
    is_creator = task.created_by == current_user.id
    is_assignee = task.assigned_to == current_user.id
    is_admin = current_user.role == "admin"
    
    # Assignee can only update status
    if is_assignee and not is_creator and not is_admin:
        if task_data.status:
            task.status = task_data.status
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Assignee can only update status"
            )
    # Creator or admin can update all fields
    elif is_creator or is_admin:
        update_data = task_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this task"
        )
    
    db.commit()
    db.refresh(task)
    
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a task"""
    task = db.query(Task).filter(Task.id == task_id).first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # Authorization: creator or admin only
    if task.created_by != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this task"
        )
    
    db.delete(task)
    db.commit()
    
    return None