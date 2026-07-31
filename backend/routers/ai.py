from fastapi import APIRouter, Depends
from database import SessionDep
from models import User, WorkoutEntry
from auth import get_current_user
from sqlmodel import select
from typing import Annotated
from dotenv import load_dotenv
import os
from google import genai

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

router = APIRouter()

@router.get('/entries/{exercise_name}/suggestion')
def get_suggestion(
    exercise_name: str,
    session: SessionDep,
    current_user: Annotated[User, Depends(get_current_user)]
):
    recent_entries = session.exec(
        select(WorkoutEntry).where(
        WorkoutEntry.exercise == exercise_name,
        WorkoutEntry.user_id == current_user.id,
    ).order_by(WorkoutEntry.id.desc()).limit(3)
    ).all()

    prompt = f"A user's last workout entries for {exercise_name}: {[(e.weight, e.reps, e.sets) for e in recent_entries]}. Suggest whether they should increase weight, reps, or stay the same, and by how much. Keep it to 1-2 sentences."
    response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=prompt,
    )
    return {"suggestion": response.text}

