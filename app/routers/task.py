from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import engine, get_db

router = APIRouter(
    prefix="/tasks",
    tags=['Tasks']
)


@router.get("/{id}", response_model=schemas.Task)
def get_task(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    task = db.query(models.Task).filter(models.Task.id == id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Task with id: {id} was not found")
    # if the user is not the one who created the task
    if task.created_by != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")
    # fetch notes
    notes = db.query(models.TaskNote).filter(
        models.TaskNote.task_id == id).all()
    task.notes = []
    for note in notes:
        task.notes.append(note.note_id)

    # fetch documents
    documents = db.query(models.TaskDocument).filter(
        models.TaskDocument.task_id == id).all()
    task.documents = []
    for document in documents:
        task.documents.append(document.document_id)

    task.members = []
    return task
    # cursor.execute("""SELECT * FROM tasks WHERE id = %s """, [str(id)])
    # task = cursor.fetchone()
    # if not task:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"Task with id: {id} was not found")
    # return {"task_detail": task}


@router.get("/", response_model=List[schemas.Task])
def get_tasks(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # to retrieve all tasks
    # tasks = db.query(models.Task).all()
    # to retrieve all tasks of the logged in user
    tasks = db.query(models.Task).filter(
        models.Task.created_by == current_user.id).filter(models.Task.title.contains(search)).limit(limit).offset(skip).all()
    return tasks
    # cursor.execute("""SELECT * FROM tasks""")
    # tasks = cursor.fetchall()
    # return {"data": tasks}


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Task)
def create_tasks(task: schemas.TaskCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_task = models.Task(created_by=current_user.id, **task.dict())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task
    # cursor.execute("""INSERT INTO tasks(title, description, created_by) VALUES(%s, %s, %s) RETURNING *""",
    #                (task.title, task.description, task.created_by))
    # new_task = cursor.fetchone()
    # conn.commit()
    # return {"data": new_task}


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    task_query = db.query(models.Task).filter(models.Task.id == id)
    task = task_query.first()
    # if task does not exist
    if task == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Task with id: {id} does not exist")
    # if the user is not the one who created the task
    if task.created_by != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")
    task_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    # cursor.execute(
    #     """DELETE FROM tasks where id = %s RETURNING *""", [str(id)])
    # deleted_task = cursor.fetchone()
    # conn.commit()
    # if deleted_task == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"Task with id: {id} does not exist")
    # return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Task)
def update_task(id: int, task: schemas.TaskCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    task_query = db.query(models.Task).filter(models.Task.id == id)
    updated_task = task_query.first()
    # if task does not exist
    if updated_task == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Task with id: {id} does not exist")
    # if the user is not the one who created the task
    if updated_task.created_by != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")
    task_query.update(task.dict(), synchronize_session=False)
    db.commit()
    return task_query.first()

    # cursor.execute(
    #     """UPDATE tasks SET title = %s, description = %s, created_by = %s where id = %s RETURNING *""", [task.title, task.description, task.created_by, str(id)])
    # updated_task = cursor.fetchone()
    # conn.commit()
    # if updated_task == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"Task with id: {id} does not exist")
    # return {'data': updated_task}


@router.post("/attach/notes", response_model=schemas.TaskNoteBase)
def attach_notes(tasknote: schemas.TaskNoteBase, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # check if task exists
    task = db.query(models.Task).filter(
        models.Task.id == tasknote.task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Task with id: {tasknote.task_id} was not found")
    # check if note exists
    note = db.query(models.Note).filter(
        models.Note.id == tasknote.note_id).first()
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Note with id: {tasknote.note_id} was not found")
    new_tasknote = models.TaskNote(**tasknote.dict())
    db.add(new_tasknote)
    db.commit()
    db.refresh(new_tasknote)
    return new_tasknote


@router.delete("/attach/notes", status_code=status.HTTP_204_NO_CONTENT)
def remove_notes(tasknote: schemas.TaskNoteBase, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    tasknote_query = db.query(models.TaskNote).filter(models.TaskNote.task_id ==
                                                      tasknote.task_id and models.TaskNote.note_id == tasknote.note_id)
    attached_note = tasknote_query.first()
    # if relationship does not exist
    if attached_note == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Record does not exist")
    tasknote_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/attach/documents", response_model=schemas.TaskDocumentBase)
def attach_documents(taskdocument: schemas.TaskDocumentBase, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # check if task exists
    task = db.query(models.Task).filter(
        models.Task.id == taskdocument.task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Task with id: {taskdocument.task_id} was not found")
    # check if document exists
    document = db.query(models.Document).filter(
        models.Document.id == taskdocument.document_id).first()
    if not document:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Document with id: {taskdocument.document_id} was not found")
    new_taskdocument = models.TaskDocument(**taskdocument.dict())
    db.add(new_taskdocument)
    db.commit()
    db.refresh(new_taskdocument)
    return new_taskdocument


@router.delete("/attach/documents", status_code=status.HTTP_204_NO_CONTENT)
def remove_documents(taskdocument: schemas.TaskDocumentBase, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    taskdocument_query = db.query(models.TaskDocument).filter(models.TaskDocument.task_id ==
                                                              taskdocument.task_id and models.TaskDocument.document_id == taskdocument.document_id)
    attached_document = taskdocument_query.first()
    # if relationship does not exist
    if attached_document == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Record does not exist")
    taskdocument_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
