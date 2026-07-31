from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from database import SessionDep
from models import User
from schemas import UserCreate, UserPublic
from auth import get_password_hash, verify_password, create_access_token
from sqlmodel import select
from typing import Annotated

class Token(BaseModel):
    access_token: str
    token_type: str

router = APIRouter()

@router.post('/register', response_model=UserPublic)
def register(user: UserCreate, session: SessionDep):
    existing = session.exec(select(User).where(User.username == user.username)).first()
    if existing:
        raise HTTPException(status_code=400, detail='Username already registered')
    hashed_password = get_password_hash(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

@router.post('/login')
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep) -> Token:
    user = session.exec(select (User).where(User.username == form_data.username)).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail='Incorrect username or password')
    access_token = create_access_token(data={'sub':user.username})
    return Token(access_token=access_token, token_type='bearer')
