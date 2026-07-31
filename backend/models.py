from typing import Optional
from sqlmodel import Field, Relationship
from schemas import UserBase, WorkoutEntryBase, SplitBase
from sqlmodel import SQLModel

class User(UserBase, table = True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str

    entries: list["WorkoutEntry"] = Relationship(back_populates="user")
    splits: list["Split"] = Relationship(back_populates="user")

class WorkoutEntry(WorkoutEntryBase, table = True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates='entries')

class SplitBase(SQLModel):
    name: str

class Split(SplitBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    user: Optional["User"] = Relationship(back_populates="splits")