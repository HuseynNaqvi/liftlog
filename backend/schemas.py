from sqlmodel import Field, SQLModel

class UserBase(SQLModel):
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True ,index=True)

class UserCreate(UserBase):
    password: str


class UserPublic(UserBase):
    id: int

class WorkoutEntryBase(SQLModel):
    exercise: str
    weight: float
    reps: int
    sets: int

class WorkoutEntryCreate(WorkoutEntryBase):
    pass

class WorkoutEntryPublic(WorkoutEntryBase):
    id: int

class SplitBase(SQLModel):
    name: str

class SplitCreate(SplitBase):
    pass

class SplitPublic(SplitBase):
    id: int