from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import time
from app.database.db import get_db
from app.schemas.user_schemas import UserCreate, UserUpdate, UserResponse
from app.services.user_service import create_user, update_user, get_user, delete_user
import asyncio
from app.services.astro_prompt_service import astro_user_report


router = APIRouter()

@router.post("/create_users/")
async def create_user_api(user: UserCreate, db: Session = Depends(get_db)):
    """
    
    The Format of Data and time should be correct 
    "date_of_birth": "1990-01-15" 
    "time_of_birth": "14:30",// Time (24-hour format)
    "place_of_birth": "Agra" 
    """
    # Create the user
    new_user = create_user(db, user)
    
    # Trigger astro_user_report function directly from astro_router
    astro_data = astro_user_report(new_user.id, db)

    # Return response in the expected format
    return {
        "id": new_user.id,
        "name": new_user.name,
        "email": new_user.email,
        "astrological_data": astro_data
    }











#other api is stopped just for time being 

# @router.get("/users/{user_id}", response_model=UserResponse)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = get_user(db, user_id)
#     if not db_user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user

# @router.put("/users/{user_id}", response_model=UserResponse)
# def update_user_api(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
#     db_user = update_user(db, user_id, user)
#     if not db_user:
#         raise HTTPException(status_code=404, detail="User not found or update failed")
#     return db_user

# @router.delete("/users/{user_id}", response_model=dict)
# def delete_user_api(user_id: int, db: Session = Depends(get_db)):
#     success = delete_user(db, user_id)
#     if not success:
#         raise HTTPException(status_code=404, detail="User not found or delete failed")
#     return {"message": "User deleted successfully"}
