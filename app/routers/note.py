from datetime import datetime, timezone
from typing import List, Optional
from fastapi import Query, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import engine, get_db

router = APIRouter(
    prefix="/notes",
    tags=['Notes']
)


@router.get("/attached", response_model=List[schemas.Note])
def get_attached_notes(noteId: list[int] = Query(default=[]), db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    notes = db.query(models.Note).filter(models.Note.id.in_(noteId)).all()
    for note in notes:
        note.created_by_user = db.query(models.User).filter(
            models.User.id == note.created_by).first()
        if note.last_updated_by is not None:
            note.last_updated_by_user = db.query(models.User).filter(
                models.User.id == note.last_updated_by).first()
    return notes


@router.get("/{id}", response_model=schemas.Note)
def get_note(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    note = db.query(models.Note).filter(models.Note.id == id).first()
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"note with id: {id} was not found")

    current_member = db.query(models.Member).filter(
        (models.Member.user_id == current_user.id) & (models.Member.project_id == note.project_id)).first()
    note.current_user_role = current_member.role

    note.created_by_user = db.query(models.User).filter(
        models.User.id == note.created_by).first()
    if note.last_updated_by is not None:
        note.last_updated_by_user = db.query(models.User).filter(
            models.User.id == note.last_updated_by).first()
    return note


@router.get("/project/{task_id}/{project_id}", response_model=List[schemas.Note])
def get_project_notes(task_id: int, project_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    notes = db.query(models.Note).filter(
        models.Note.project_id == project_id).all()
    project_notes = []
    for note in notes:
        tasknote = db.query(models.TaskNote).filter(
            (models.TaskNote.task_id == task_id) & (models.TaskNote.note_id == note.id)).first()
        if not tasknote:
            note.created_by_user = db.query(models.User).filter(
                models.User.id == note.created_by).first()
            if note.last_updated_by is not None:
                note.last_updated_by_user = db.query(models.User).filter(
                    models.User.id == note.last_updated_by).first()
            project_notes.append(note)
    return project_notes


@router.get("/project/{project_id}", response_model=List[schemas.Note])
def get_notes(project_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), search: Optional[str] = ""):
    notes = db.query(models.Note).filter(
        models.Note.project_id == project_id).filter(models.Note.title.contains(search)).all()
    for note in notes:
        note.created_by_user = db.query(models.User).filter(
            models.User.id == note.created_by).first()
        if note.last_updated_by is not None:
            note.last_updated_by_user = db.query(models.User).filter(
                models.User.id == note.last_updated_by).first()
    return notes


@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=schemas.Note)
def create_notes(note: schemas.NoteCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_note = models.Note(created_by=current_user.id, **note.dict())
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    new_note.created_by_user = db.query(models.User).filter(
        models.User.id == new_note.created_by).first()
    if new_note.last_updated_by is not None:
        new_note.last_updated_by_user = db.query(models.User).filter(
            models.User.id == new_note.last_updated_by).first()
    return new_note


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    note_query = db.query(models.Note).filter(models.Note.id == id)
    note = note_query.first()
    # if note does not exist
    if note == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"note with id: {id} does not exist")
    note_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Note)
def update_note(id: int, note: schemas.NoteCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    note_query = db.query(models.Note).filter(models.Note.id == id)
    existing_note = note_query.first()
    # if note does not exist
    if existing_note == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"note with id: {id} does not exist")
    # # if the user is not the one who created the note
    # if updated_note.created_by != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                         detail=f"Not authorized to perform requested action")
    note.updated_at = datetime.now(timezone.utc).isoformat()
    note.last_updated_by = current_user.id
    note_query.update(note.dict(), synchronize_session=False)
    db.commit()

    updated_note = note_query.first()
    updated_note.created_by_user = db.query(models.User).filter(
        models.User.id == updated_note.created_by).first()
    if updated_note.last_updated_by is not None:
        updated_note.last_updated_by_user = db.query(models.User).filter(
            models.User.id == updated_note.last_updated_by).first()
    return updated_note
