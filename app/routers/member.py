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
                status=member.status,
                user=schemas.UserOut(id=user.id, email=user.email,
                                     created_at=user.created_at),
            )
            invitedMembers.append(memberOut)
    return invitedMembers
