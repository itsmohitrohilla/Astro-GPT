from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.database.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    year = Column(Integer)
    month = Column(Integer)
    date = Column(Integer)
    hours = Column(Integer)
    minutes = Column(Integer)
    seconds = Column(Integer, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    timezone = Column(Float, default=5.5)
