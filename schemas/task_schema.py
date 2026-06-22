from pydantic import BaseModel
from datetime import date, datetime
from models.task import TaskStatus, TaskPriority
from typing import Optional
from schemas.user_schema import UserResponseModel

class TaskCreateReqModel(BaseModel):
    title: str
    description: Optional[str] = None
    priority: TaskPriority = TaskPriority.low
    sprint_id: int

class TaskResponseModel(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: TaskStatus
    priority: TaskPriority
    assignee_id: Optional[int]
    sprint_id: int
    created_at: datetime

    model_config = {"from_attributes": True}

class TaskAssignReqModel(BaseModel):
    assignee_id: int  

class TaskStatusUpdateReqModel(BaseModel):
    status: TaskStatus

class TaskWithAssigneeResponseModel(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: TaskStatus
    priority: TaskPriority
    assignee: Optional[UserResponseModel] = None

    model_config = {"from_attributes": True}