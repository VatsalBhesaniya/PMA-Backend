
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    username: str
    first_name: str
    last_name: str
    created_at: datetime = datetime.utcnow()


class UserUpdate(BaseModel):
    email: EmailStr
    username: str
    first_name: str
    last_name: str


class UserPasswordUpdate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    created_at: datetime

    class Config:
        orm_mode = True


class ProjectBase(BaseModel):
    title: str
    created_at: datetime = datetime.utcnow()


class ProjectCreate(ProjectBase):
    pass


class MilestoneBase(BaseModel):
    project_id: int
    title: str
    description: list = None
    description_plain_text: str = None
    is_completed: bool
    completion_date: datetime


class MilestoneCreate(MilestoneBase):
    pass


class MilestoneOut(MilestoneBase):
    id: int

    class Config:
        orm_mode = True


class MilestonesOut(BaseModel):
    milestones: list[MilestoneOut] = []
    current_user_role: int

    class Config:
        orm_mode = True


class MemberBase(BaseModel):
    user_id: int
    project_id: int
    role: int
    created_at: datetime = datetime.utcnow()

    class Config:
        orm_mode = True


class TaskBase(BaseModel):
    project_id: int
    title: str
    description: list = None
    description_plain_text: str = None
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = None
    last_updated_by: int = None
    status = 1


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    id: int
    created_by: int = None
    members: list = []
    notes: list = []
    documents: list = []
    owner: UserOut

    class Config:
        orm_mode = True


class TaskDetail(TaskBase):
    id: int
    created_by: int = None
    members: list = []
    notes: list = []
    documents: list = []
    owner: UserOut
    current_user_role: int

    class Config:
        orm_mode = True


class TaskNoteBase(BaseModel):
    task_id: int
    note_id: int

    class Config:
        orm_mode = True


class TaskDocumentBase(BaseModel):
    task_id: int
    document_id: int

    class Config:
        orm_mode = True


class NoteBase(BaseModel):
    project_id: int
    title: str
    content: list = None
    content_plain_text: str = None
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = None
    last_updated_by: int = None


class NoteCreate(NoteBase):
    pass


class DocumentBase(BaseModel):
    project_id: int
    title: str
    content: list = None
    content_plain_text: str = None
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = None
    last_updated_by: int = None


class DocumentCreate(DocumentBase):
    pass


class SearchUsersOut(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True


class MemberOut(MemberBase):
    user: UserOut

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
    current_user_role: int = None

    class Config:
        orm_mode = True


class ProjectDetailOut(ProjectBase):
    id: int
    created_at: datetime
    created_by: int
    members: list[MemberOut]
    current_user_role: int = None

    class Config:
        orm_mode = True


class Note(NoteBase):
    id: int
    created_by: int
    created_by_user: UserOut
    last_updated_by_user: UserOut = None
    current_user_role: int = None

    class Config:
        orm_mode = True


class Document(DocumentBase):
    id: int
    created_by: int = None
    created_by_user: UserOut
    last_updated_by_user: UserOut = None
    current_user_role: int = None

    class Config:
        orm_mode = True
