from fastapi import FastAPI
from database import create_db_and_tables
from contextlib import asynccontextmanager
from routers import users
from routers import entries
from routers import ai
from routers import splits
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(users.router)
app.include_router(entries.router)
app.include_router(ai.router)
app.include_router(splits.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)