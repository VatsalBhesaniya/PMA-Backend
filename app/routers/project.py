from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import engine, get_db

router = APIRouter(
    prefix="/projects",
    tags=['Projects']
)


@router.get("/invited", response_model=List[schemas.ProjectOut])
def get_projects_invited(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    members = db.query(models.Member).filter(
        (models.Member.user_id == current_user.id) & (models.Member.role != 1)).all()
    projects = []
    for member in members:
        project = db.query(models.Project).filter(
            models.Project.id == member.project_id).first()
        projects.append(project)
    return projects


@router.get("/members/{id}", response_model=List[schemas.SearchUsersOut])
def get_project_members(id: int, search: str, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    members = db.query(models.Member).filter(
        models.Member.project_id == id).all()
    users = []
    for member in members:
        user = db.query(models.User).filter(
            models.User.id == member.user_id).filter(
            models.User.username.ilike('%' + search.lower() + '%')).first()
        if user != None:
            users.append(user)
    return users


@router.get("/{id}", response_model=schemas.ProjectOut)
def get_project(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    project = db.query(models.Project).filter(models.Project.id == id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Project with id: {id} was not found")
    return project


@router.get("/detail/{id}", response_model=schemas.ProjectDetailOut)
def get_project_detail(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    project = db.query(models.Project).filter(models.Project.id == id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Project with id: {id} was not found")
    members = db.query(models.Member).filter(
        models.Member.project_id == project.id).all()
    project.members = []
    for member in members:
        user = db.query(models.User).filter(
            models.User.id == member.user_id).first()
        memberOut = schemas.MemberOut(
            user_id=member.user_id,
            project_id=member.project_id,
            role=member.role,
            created_at=member.created_at,
            user=schemas.UserOut(id=user.id, email=user.email, username=user.username, first_name=user.first_name,
                                 last_name=user.last_name, created_at=user.created_at),
        )
        project.members.append(memberOut)
    return project


@router.get("/", response_model=List[schemas.ProjectOut])
def get_projects(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    projects = db.query(models.Project).filter(
        models.Project.created_by == current_user.id).filter(models.Project.title.contains(search)).limit(limit).offset(skip).all()
    return projects


@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=schemas.ProjectOut)
def create_projects(project: schemas.ProjectCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_project = models.Project(created_by=current_user.id, **project.dict())
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    role = db.get(models.Role, 1)
    new_member = models.Member(user_id=current_user.id,
                               project_id=new_project.id, role=role.id, status=1)
    db.add(new_member)
    db.commit()
    return new_project


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    project_query = db.query(models.Project).filter(models.Project.id == id)
    project = project_query.first()
    # if project does not exist
    if project == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Project with id: {id} does not exist")
    # if the user is not the one who created the project
    if project.created_by != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")
    project_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.ProjectOut)
def update_project(id: int, project: schemas.ProjectCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    project_query = db.query(models.Project).filter(models.Project.id == id)
    updated_project = project_query.first()
    # if project does not exist
    if updated_project == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Project with id: {id} does not exist")
    # if the user is not the one who created the project
    if updated_project.created_by != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")
    project_query.update(project.dict(), synchronize_session=False)
    db.commit()
    return project_query.first()
