
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# Request Models


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class ProjectBase(BaseModel):
    title: str
    created_at: datetime = datetime.utcnow()


class ProjectCreate(ProjectBase):
    pass


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


class NoteBase(BaseModel):
    title: str
    description: str
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = None
    last_updated_by: int = None


class NoteCreate(NoteBase):
    pass


class DocumentBase(BaseModel):
    title: str
    content: str
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = None
    last_updated_by: int = None


class DocumentCreate(DocumentBase):
    pass

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


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class ProjectOut(ProjectBase):
    id: int
    created_at: datetime
    created_by: int

    class Config:
        orm_mode = True


class Task(TaskBase):
    id: int
    created_at: datetime
    created_by: int = None
    owner: UserOut

    class Config:
        orm_mode = True


class Note(NoteBase):
    id: int
    created_by: int = None

    class Config:
        orm_mode = True


class Document(DocumentBase):
    id: int
    created_by: int = None

    class Config:
        orm_mode = True
