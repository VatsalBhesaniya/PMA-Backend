from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import engine, get_db

router = APIRouter(
    prefix="/documents",
    tags=['Documents']
)


@router.get("/{id}", response_model=schemas.Document)
def get_document(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    document = db.query(models.Document).filter(
        models.Document.id == id).first()
    if not document:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"document with id: {id} was not found")
    # if the user is not the one who created the document
    if document.created_by != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")
    return document


@router.get("/", response_model=List[schemas.Document])
def get_documents(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    documents = db.query(models.Document).filter(
        models.Document.created_by == current_user.id).filter(models.Document.title.contains(search)).limit(limit).offset(skip).all()
    return documents


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Document)
def create_documents(document: schemas.DocumentCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_document = models.Document(
        created_by=current_user.id, **document.dict())
    db.add(new_document)
    db.commit()
    db.refresh(new_document)
    return new_document


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    document_query = db.query(models.Document).filter(models.Document.id == id)
    document = document_query.first()
    # if document does not exist
    if document == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"document with id: {id} does not exist")
    # if the user is not the one who created the document
    if document.created_by != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")
    document_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Document)
def update_document(id: int, document: schemas.DocumentCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    document_query = db.query(models.Document).filter(models.Document.id == id)
    updated_document = document_query.first()
    # if document does not exist
    if updated_document == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"document with id: {id} does not exist")
    # if the user is not the one who created the document
    if updated_document.created_by != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")
    document_query.update(document.dict(), synchronize_session=False)
    db.commit()
    return document_query.first()
