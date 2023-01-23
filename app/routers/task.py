from typing import List, Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
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
                            detail=f"post with id: {id} was not found")
    # if the user is not the one who created the task
    if task.created_by != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")
    return task
    # cursor.execute("""SELECT * FROM tasks WHERE id = %s """, [str(id)])
    # task = cursor.fetchone()
    # if not task:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"post with id: {id} was not found")
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
                            detail=f"post with id: {id} does not exist")
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
    #                         detail=f"post with id: {id} does not exist")
    # return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Task)
def update_task(id: int, task: schemas.TaskCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    task_query = db.query(models.Task).filter(models.Task.id == id)
    updated_task = task_query.first()
    # if task does not exist
    if updated_task == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
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
    #                         detail=f"post with id: {id} does not exist")
    # return {'data': updated_task}
