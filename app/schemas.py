
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
    created_by: int


class TaskCreate(TaskBase):
    pass


class UserCreate(BaseModel):
    email: EmailStr
    password: str


# Response Models
# https: // fastapi.tiangolo.com/tutorial/sql-databases/  # __tabbed_1_3


class Task(TaskBase):
    class Config:
        orm_mode = True


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
