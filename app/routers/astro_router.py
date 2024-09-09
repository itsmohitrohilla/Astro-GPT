from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database.db import get_db
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from app.services.astro_prompt_service import fetch_astro_info
from app.services.astro_gpt import astro_gpt_llm
from app.models.user_model import User

router = APIRouter()

class QueryRequest(BaseModel):
    query: str

@router.post("/astro-user-data")
def astro_user_report(user_id: int, db: Session = Depends(get_db)):
    try:
        astro_data = fetch_astro_info(user_id)
        
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user.astro_data = astro_data

        db.commit()
        db.refresh(user)
        
        return {"message": "Astro data updated successfully! Now you can use Astro-GPT "}

    except Exception as e:
        db.rollback() 
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.post("/astro-gpt")
def astro_gpt_route(user_id: int, query: QueryRequest, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        pre_prompt = user.astro_data
        
        if isinstance(pre_prompt, dict) and 'error' in pre_prompt:
            raise HTTPException(status_code=400, detail=pre_prompt['error'])
        
        if isinstance(pre_prompt, str) and pre_prompt == "User not found":
            raise HTTPException(status_code=404, detail="User not found")
        
        astrogpt_response = astro_gpt_llm(pre_prompt, query.query)
        
        personalized_prompt_response = f"{user.name}, here is your astrological Response: {astrogpt_response}"
        
        return {
            "message": personalized_prompt_response
        }
    
    except HTTPException as e:
        raise e
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
