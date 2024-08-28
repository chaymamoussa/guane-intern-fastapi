from typing import Any, Optional
from pydantic import BaseModel
from typing import List
from datetime import datetime



class CeleryTaskResponse(BaseModel):
    task_complexity: int
    status: str = 'Successfully submitted the task.'
    server_message: Optional[Any]
    success: bool = True

class TaskStatusResponse(BaseModel):
    task_id: str
    status: str
    result: Optional[Any]
    date_done: Optional[str]
    traceback: Optional[str]

class TaskListResponse(BaseModel):
    tasks: List[TaskStatusResponse]


class TaskBase(BaseModel):
    name: str
    description: Optional[str] = None
    status: Optional[str] = 'pending'  # Default status if not provided

class TaskCreate(TaskBase):
    pass

class TaskInDBBase(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime

class Task(TaskInDBBase):
    pass
class Tasks(BaseModel):
    tasks: List[Task]


class TaskUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None







