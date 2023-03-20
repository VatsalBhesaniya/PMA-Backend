from datetime import datetime, timezone
from typing import List, Optional
from fastapi import Query, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import engine, get_db

router = APIRouter(
    prefix="/documents",
    tags=['Documents']
)


@router.get("/attached", response_model=List[schemas.Document])
def get_attached_documents(documentId: list[int] = Query(default=[]), db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    documents = db.query(models.Document).filter(
        models.Document.id.in_(documentId)).all()
    for document in documents:
        document.created_by_user = db.query(models.User).filter(
            models.User.id == document.created_by).first()
        if document.last_updated_by is not None:
            document.last_updated_by_user = db.query(models.User).filter(
                models.User.id == document.last_updated_by).first()
    return documents


@router.get("/{id}", response_model=schemas.Document)
def get_document(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    document = db.query(models.Document).filter(
        models.Document.id == id).first()
    if not document:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"document with id: {id} was not found")

    current_member = db.query(models.Member).filter(
        (models.Member.user_id == current_user.id) & (models.Member.project_id == document.project_id)).first()
    document.current_user_role = current_member.role

    document.created_by_user = db.query(models.User).filter(
        models.User.id == document.created_by).first()
    if document.last_updated_by is not None:
        document.last_updated_by_user = db.query(models.User).filter(
            models.User.id == document.last_updated_by).first()
    return document


@router.get("/project/{task_id}/{project_id}", response_model=List[schemas.Document])
def get_project_documents(task_id: int, project_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    documents = db.query(models.Document).filter(
        models.Document.project_id == project_id).all()
    project_documents = []
    for document in documents:
        taskdocument = db.query(models.TaskDocument).filter(
            (models.TaskDocument.task_id == task_id) & (models.TaskDocument.document_id == document.id)).first()
        if not taskdocument:
            document.created_by_user = db.query(models.User).filter(
                models.User.id == document.created_by).first()
            if document.last_updated_by is not None:
                document.last_updated_by_user = db.query(models.User).filter(
                    models.User.id == document.last_updated_by).first()
            project_documents.append(document)
    return project_documents


@router.get("/project/{project_id}", response_model=List[schemas.Document])
def get_documents(project_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), search: Optional[str] = ""):
    documents = db.query(models.Document).filter(
        models.Document.project_id == project_id).filter(models.Document.title.contains(search)).all()
    for document in documents:
        document.created_by_user = db.query(models.User).filter(
            models.User.id == document.created_by).first()
        if document.last_updated_by is not None:
            document.last_updated_by_user = db.query(models.User).filter(
                models.User.id == document.last_updated_by).first()
    return documents


@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=schemas.Document)
def create_documents(document: schemas.DocumentCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_document = models.Document(
        created_by=current_user.id, **document.dict())
    db.add(new_document)
    db.commit()
    db.refresh(new_document)
    new_document.created_by_user = db.query(models.User).filter(
        models.User.id == new_document.created_by).first()
    if new_document.last_updated_by is not None:
        new_document.last_updated_by_user = db.query(models.User).filter(
            models.User.id == new_document.last_updated_by).first()
    return new_document


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    document_query = db.query(models.Document).filter(models.Document.id == id)
    document = document_query.first()
    # if document does not exist
    if document == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"document with id: {id} does not exist")
    document_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Document)
def update_document(id: int, document: schemas.DocumentCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    document_query = db.query(models.Document).filter(models.Document.id == id)
    existing_document = document_query.first()
    # if document does not exist
    if existing_document == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"document with id: {id} does not exist")
    document.updated_at = datetime.now(timezone.utc).isoformat()
    document.last_updated_by = current_user.id
    document_query.update(document.dict(), synchronize_session=False)
    db.commit()

    update_document = document_query.first()
    update_document.created_by_user = db.query(models.User).filter(
        models.User.id == update_document.created_by).first()
    if update_document.last_updated_by is not None:
        update_document.last_updated_by_user = db.query(models.User).filter(
            models.User.id == update_document.last_updated_by).first()
    return update_document
