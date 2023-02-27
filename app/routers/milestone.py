from typing import List
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import engine, get_db

router = APIRouter(
    prefix="/milestones",
    tags=['Milestones']
)


@router.get("/{id}", response_model=schemas.MilestoneOut)
def get_milestone(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    milestone = db.query(models.Milestone).filter(
        (models.Milestone.id == id)).first()
    if not milestone:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Milestone with id: {id} was not found")
    return milestone


@router.get("/project/{id}", response_model=List[schemas.MilestoneOut])
def get_milestones(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    milestones = db.query(models.Milestone).filter(
        (models.Milestone.project_id == id)).all()
    return milestones


@router.post("/create", response_model=schemas.MilestoneOut)
def create_milestones(milestone: schemas.MilestoneCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_milestone = models.Milestone(**milestone.dict())
    db.add(new_milestone)
    db.commit()
    db.refresh(new_milestone)
    return new_milestone


@router.put("/{id}", response_model=schemas.MilestoneOut)
def update_milestones(id: int, milestone: schemas.MilestoneCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    milestone_query = db.query(models.Milestone).filter(
        models.Milestone.id == id)
    updated_milestone = milestone_query.first()
    # if milestone does not exist
    if updated_milestone == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Milestone with id: {id} does not exist")
    milestone_query.update(milestone.dict(), synchronize_session=False)
    db.commit()
    return milestone_query.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_milestone(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    milestone_query = db.query(models.Milestone).filter(
        models.Milestone.id == id)
    milestone = milestone_query.first()
    # if milestone does not exist
    if milestone == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Milestone with id: {id} does not exist")
    milestone_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
