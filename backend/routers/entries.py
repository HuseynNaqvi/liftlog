from fastapi import APIRouter, Depends, HTTPException
from database import SessionDep
from models import User, WorkoutEntry
from schemas import WorkoutEntryCreate, WorkoutEntryPublic
from auth import get_current_user
from sqlmodel import select
from typing import Annotated


router = APIRouter()

@router.post('/entries', response_model=WorkoutEntryPublic)
def create_entry(
    entry: WorkoutEntryCreate,                              
    session: SessionDep,                                    
    current_user: Annotated[User, Depends(get_current_user)] 
):
    new_entry = WorkoutEntry(
        exercise=entry.exercise,
        weight=entry.weight,
        reps=entry.reps,
        sets=entry.sets,
        user_id=current_user.id,
    )  
    session.add(new_entry)
    session.commit()
    session.refresh(new_entry)
    return new_entry


@router.get('/entries', response_model=list[WorkoutEntryPublic])
def get_entries(
    session: SessionDep,
    current_user: Annotated[User, Depends(get_current_user)]
):
    entries = session.exec(
        select(WorkoutEntry).where(WorkoutEntry.user_id == current_user.id) 
    ).all()
    return entries

@router.put('/entries/{entry_id}', response_model=WorkoutEntryPublic)
def update_entry(
    entry_id: int,
    updated: WorkoutEntryCreate,
    session: SessionDep,
    current_user: Annotated[User, Depends(get_current_user)]
):
    entry = session.get(WorkoutEntry, entry_id)
    if not entry or entry.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Entry not found")
    entry.exercise = updated.exercise
    entry.weight = updated.weight
    entry.reps = updated.reps
    entry.sets = updated.sets
    session.add(entry)
    session.commit()
    session.refresh(entry)
    return entry


@router.delete('/entries/{entry_id}')
def delete_entry(
    entry_id: int,
    session: SessionDep,
    current_user: Annotated[User, Depends(get_current_user)]
):
    entry = session.get(WorkoutEntry, entry_id)
    if not entry or entry.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Entry not found")
    session.delete(entry)
    session.commit()
    return {"message": "Entry deleted"}