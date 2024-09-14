from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.services.astro_gpt import astro_gpt_llm_task  # Import the Celery task
from app.models.user_model import User
from redis import Redis
import asyncio

router = APIRouter()
redis_instance = Redis.from_url("redis://localhost", encoding="utf8", decode_responses=True)

class QueryRequest(BaseModel):
    query: str

# fetch astrology data from the database
def fetch_astro_data_from_db(user_id: int, db: Session) -> str:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return "User not found"
    if not user.astro_data:
        return {"error": "No astrological data found for the user"}
    return user.astro_data

@router.post("/astro-gpt")
async def astro_gpt_route(user_id: int, query: QueryRequest, db: Session = Depends(get_db)):
    try:
        # Check if user data is cached in Redis
        cached_data = redis_instance.get(f"user_{user_id}")
        if cached_data:
            pre_prompt = cached_data
        else:
            pre_prompt = fetch_astro_data_from_db(user_id, db)
            
            if isinstance(pre_prompt, dict) and 'error' in pre_prompt:
                raise HTTPException(status_code=400, detail=pre_prompt['error'])
            if isinstance(pre_prompt, str) and pre_prompt == "User not found":
                raise HTTPException(status_code=404, detail="User not found")

            redis_instance.setex(f"user_{user_id}", 604800, pre_prompt)  # Cache for 7 days

        # Trigger Celery task asynchronously and wait for the result
        task = astro_gpt_llm_task.delay(pre_prompt, query.query)

        # Wait for the task to complete (without blocking other requests)
        result = await asyncio.to_thread(task.get, timeout=25)  # Use asyncio to handle the blocking get() in a non-blocking way

        if isinstance(result, dict) and "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])

        personalized_prompt_response = f"Here is your astrological response: {result}"
        return {"message": personalized_prompt_response}

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

