from typing import Optional
from sqlmodel import Field, Relationship, SQLModel
from schemas import UserBase, WorkoutEntryBase, SplitBase

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    entries: list["WorkoutEntry"] = Relationship(back_populates="user")
    splits: list["Split"] = Relationship(back_populates="user")

class WorkoutEntry(WorkoutEntryBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates='entries')

class Split(SplitBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    user: Optional["User"] = Relationship(back_populates="splits")