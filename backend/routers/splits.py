from fastapi import APIRouter, Depends, HTTPException
from database import SessionDep
from models import User, Split
from schemas import SplitCreate, SplitPublic
from auth import get_current_user
from sqlmodel import select
from typing import Annotated

router = APIRouter()

@router.post('/splits', response_model=SplitPublic)
def create_split(split: SplitCreate, session: SessionDep, current_user: Annotated[User, Depends(get_current_user)]):
    new_split = Split(name=split.name, content=split.content, user_id=current_user.id)
    session.add(new_split)
    session.commit()
    session.refresh(new_split)
    return new_split

@router.get('/splits', response_model=list[SplitPublic])
def get_splits(session: SessionDep, current_user: Annotated[User, Depends(get_current_user)]):
    return session.exec(select(Split).where(Split.user_id == current_user.id)).all()

@router.put('/splits/{split_id}', response_model=SplitPublic)
def update_split(
    split_id: int,
    updated: SplitCreate,
    session: SessionDep,
    current_user: Annotated[User, Depends(get_current_user)]
):
    split = session.get(Split, split_id)
    if not split or split.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Split not found")
    split.name = updated.name
    split.content = updated.content
    session.add(split)
    session.commit()
    session.refresh(split)
    return split

@router.delete('/splits/{split_id}')
def delete_split(split_id: int, session: SessionDep, current_user: Annotated[User, Depends(get_current_user)]):
    split = session.get(Split, split_id)
    if not split or split.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Split not found")
    session.delete(split)
    session.commit()
    return {"message": "Split deleted"}