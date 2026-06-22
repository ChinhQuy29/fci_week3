from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from models.user import UserRole

class UserCreateReqModel(BaseModel):
    name:  str
    email: EmailStr
    role:  UserRole = UserRole.member

class UserUpdateReqModel(BaseModel):
    name:  Optional[str] = None
    email: Optional[EmailStr] = None

class UserResponseModel(BaseModel):
    id:         int
    name:       str
    email:      str
    role:       UserRole
    is_active:  bool
    created_at: datetime

    model_config = {"from_attributes": True}
