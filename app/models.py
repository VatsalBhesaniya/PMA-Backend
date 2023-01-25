from .database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP, ARRAY
from sqlalchemy.sql.expression import text


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=text('now()'), nullable=False)


class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=text('now()'), nullable=False)
    created_by = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)


class Member(Base):
    __tablename__ = "members"
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), primary_key=True)
    project_id = Column(Integer, ForeignKey(
        "projects.id", ondelete="CASCADE"), primary_key=True)
    role = Column(Integer, ForeignKey(
        "roles.id", ondelete="RESTRICT"),  nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=text('now()'), nullable=False)


class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String)
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=text('now()'), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True))
    last_updated_by = Column(Integer)
    members = Column(ARRAY(Integer))
    notes = Column(ARRAY(Integer))
    documents = Column(ARRAY(Integer))
    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    owner = relationship("User")


class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String)
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=text('now()'), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True))
    last_updated_by = Column(Integer)
    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))


class TaskNote(Base):
    __tablename__ = "tasknotes"
    task_id = Column(Integer, ForeignKey(
        "tasks.id", ondelete="CASCADE"), primary_key=True)
    note_id = Column(Integer, ForeignKey(
        "notes.id", ondelete="CASCADE"), primary_key=True)


class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String)
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=text('now()'), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True))
    last_updated_by = Column(Integer)
    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))


class TaskDocument(Base):
    __tablename__ = "taskdocuments"
    task_id = Column(Integer, ForeignKey(
        "tasks.id", ondelete="CASCADE"), primary_key=True)
    documents_id = Column(Integer, ForeignKey(
        "documents.id", ondelete="CASCADE"), primary_key=True)
