from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.schemas.user_schemas import UserCreate, UserUpdate, UserResponse
from app.services.user_service import create_user, update_user, get_user, delete_user

router = APIRouter()

@router.post("/users/", response_model=UserResponse)
def create_user_api(user: UserCreate, db: Session = Depends(get_db)):
    """
    
    The Format of Data and time should be correct 
    
    example: 
    {
        "date_of_birth": "1990-01-15",  
        "time_of_birth": "14:30",       // Time of birth in HH:MM (24-hour format)
        "place_of_birth": "Agra" 
    }
    """
    return create_user(db, user)

@router.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/users/{user_id}", response_model=UserResponse)
def update_user_api(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = update_user(db, user_id, user)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found or update failed")
    return db_user

@router.delete("/users/{user_id}", response_model=dict)
def delete_user_api(user_id: int, db: Session = Depends(get_db)):
    success = delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found or delete failed")
    return {"message": "User deleted successfully"}
