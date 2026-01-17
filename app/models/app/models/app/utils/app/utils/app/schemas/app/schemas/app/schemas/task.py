from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.schemas.user import UserResponse


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    status: Optional[str] = Field("pending", pattern="^(pending|in_progress|completed)$")
    priority: Optional[str] = Field("medium", pattern="^(low|medium|high)$")
    due_date: Optional[datetime] = None
    assigned_to: Optional[int] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    status: Optional[str] = Field(None, pattern="^(pending|in_progress|completed)$")
    priority: Optional[str] = Field(None, pattern="^(low|medium|high)$")
    due_date: Optional[datetime] = None
    assigned_to: Optional[int] = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str
    priority: str
    due_date: Optional[datetime]
    created_by: int
    assigned_to: Optional[int]
    created_at: datetime
    updated_at: datetime
    creator: Optional[UserResponse] = None
    assignee: Optional[UserResponse] = None
    
    class Config:
        from_attributes = True


class TaskStatistics(BaseModel):
    total_tasks: int
    completed_tasks: int
    pending_tasks: int
    in_progress_tasks: int
    high_priority: int
    medium_priority: int
    low_priority: int