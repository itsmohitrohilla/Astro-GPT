from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    name: str
    email: str
    date_of_birth: str  # YYYY-MM-DD
    time_of_birth: str  # (24-hour format)
    place_of_birth: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    date_of_birth: Optional[str] = None
    time_of_birth: Optional[str] = None
    place_of_birth: Optional[str] = None

class UserResponseComplete(BaseModel):
    id: int
    name: str
    email: str
    year: int
    month: int
    date: int
    hours: int
    minutes: int
    seconds: int = 0
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    timezone: float

    class Config:
        orm_mode = True

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    astro_data : str

    class Config:
        orm_mode = True