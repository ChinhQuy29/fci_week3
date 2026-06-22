from pydantic import BaseModel
from datetime import date, datetime
from models.sprint import SprintStatus
from typing import Optional
from schemas.task_schema import TaskWithAssigneeResponseModel

class SprintCreateReqModel(BaseModel):
    title: str
    from_date: date
    to_date: date

class SprintAddMemberReqModel(BaseModel):
    user_id: int

class SprintResponseModel(BaseModel):
    id: int
    title: str
    from_date: date
    to_date: date
    status: SprintStatus
    created_at: datetime
    created_by: int

    model_config = {"from_attributes": True}

class SprintWithTaskResponseModel(BaseModel):
    tasks: list[TaskWithAssigneeResponseModel] = []

