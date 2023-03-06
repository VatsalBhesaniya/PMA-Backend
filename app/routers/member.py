from typing import List, Optional
from fastapi import Query, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import engine, get_db

router = APIRouter(
    prefix="/members",
    tags=['members']
)


@router.post("/invite", response_model=List[schemas.MemberOut])
def invite_members(members: list[schemas.MemberBase], db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    invitedMembers = []
    for member in members:
        existingMember = db.query(models.Member).where(
            (models.Member.user_id == member.user_id) & (models.Member.project_id == member.project_id)).first()
        if existingMember == None:
            new_member = models.Member(**member.dict())
            db.add(new_member)
            db.commit()
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
            invitedMembers.append(memberOut)
    return invitedMembers


@router.delete("/{project_id}/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_member(user_id: int, project_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    member_query = db.query(models.Member).filter((models.Member.user_id == user_id) & (
        models.Member.project_id == project_id))
    member = member_query.first()
    # if member does not exist
    if member == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"member with id: {user_id} does not exist")
    member_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
