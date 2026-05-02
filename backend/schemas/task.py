from pydantic import BaseModel
from typing import Optional
from enum import Enum


class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = ""
    priority: Priority = Priority.medium
    deadline: Optional[str] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[Priority] = None
    completed: Optional[bool] = None
    deadline: Optional[str] = None
