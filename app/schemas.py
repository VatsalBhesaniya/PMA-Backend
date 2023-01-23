
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# Request Models


class TaskBase(BaseModel):
    title: str
    description: str
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = None
    last_updated_by: int = None
    members: list = None
    notes: list = None
    documents: list = None


class TaskCreate(TaskBase):
    pass


class UserCreate(BaseModel):
    email: EmailStr
    password: str


# Response Models
# https: // fastapi.tiangolo.com/tutorial/sql-databases/  # __tabbed_1_3


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Task(TaskBase):
    id: int
    created_at: datetime
    created_by: int = None
    owner: UserOut

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
