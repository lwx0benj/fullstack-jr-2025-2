from datetime import date, datetime

from pydantic import BaseModel
from typing import Optional
from backend.models.users import TaskPriority, TaskStatus


class TaskBaseSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[TaskPriority] = None
    status: Optional[TaskStatus] = None
    due_date: Optional[date] = None


class TaskCreateSchema(TaskBaseSchema):
    title: str


class TaskUpdateSchema(TaskBaseSchema):
    pass


class TaskStatusSchema(BaseModel):
    status: TaskStatus


class TaskOutSchema(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: TaskStatus
    priority: TaskPriority
    due_date: Optional[date] = None
    created_at: datetime
    updated_at: datetime
