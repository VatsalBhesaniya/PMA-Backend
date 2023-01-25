from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import engine, get_db

router = APIRouter(
    prefix="/notes",
    tags=['Notes']
)


@router.get("/{id}", response_model=schemas.Note)
def get_note(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    note = db.query(models.Note).filter(models.Note.id == id).first()
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"note with id: {id} was not found")
    # if the user is not the one who created the note
    if note.created_by != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")
    return note


@router.get("/", response_model=List[schemas.Note])
def get_notes(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    notes = db.query(models.Note).filter(
        models.Note.created_by == current_user.id).filter(models.Note.title.contains(search)).limit(limit).offset(skip).all()
    return notes


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Note)
def create_notes(note: schemas.NoteCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_note = models.Note(created_by=current_user.id, **note.dict())
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    note_query = db.query(models.Note).filter(models.Note.id == id)
    note = note_query.first()
    # if note does not exist
    if note == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"note with id: {id} does not exist")
    # if the user is not the one who created the note
    if note.created_by != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")
    note_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Note)
def update_note(id: int, note: schemas.NoteCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    note_query = db.query(models.Note).filter(models.Note.id == id)
    updated_note = note_query.first()
    # if note does not exist
    if updated_note == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"note with id: {id} does not exist")
    # if the user is not the one who created the note
    if updated_note.created_by != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")
    note_query.update(note.dict(), synchronize_session=False)
    db.commit()
    return note_query.first()
