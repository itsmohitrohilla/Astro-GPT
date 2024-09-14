from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderQuotaExceeded, GeocoderServiceError
import ssl
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from geopy.exc import GeocoderTimedOut
from app.models.user_model import User
from app.schemas.user_schemas import UserCreate, UserUpdate


# Disable SSL verification for Nominatim (not recommended for production)
try:
    _create_default_https_context = ssl._create_default_https_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = ssl._create_unverified_context


def get_lat_long(place_name):
    # Initialize Nominatim API with a user agent
    geolocator = Nominatim(user_agent="mrohilla165@gmail.com")
    
    try:
        # Get location
        location = geolocator.geocode(place_name, timeout=10)
        if location:
            return round(location.latitude, 4), round(location.longitude, 4)
        else:
            return None, None
    except GeocoderTimedOut:
        print("Geocoding service timed out. Try again later.")
        return None, None
    except GeocoderQuotaExceeded:
        print("Geocoding quota exceeded. Please try again later.")
        return None, None
    except GeocoderServiceError as e:
        print(f"Geocoding service error: {e}")
        return None, None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None, None


def parse_time(time_str: str):
    """Parse time string in HH:MM format and return hours, minutes, and default seconds."""
    hours, minutes = map(int, time_str.split(':'))
    return hours, minutes, 0  # Seconds default to 0

def create_user(db: Session, user: UserCreate):
    """Create a new user in the database."""
    
    # Check if a user with the same email already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise ValueError("A user with this email already exists.")
    
    try:
        # Extract date, time, and location from user input
        year, month, date = map(int, user.date_of_birth.split('-'))
        hours, minutes, seconds = parse_time(user.time_of_birth)
        latitude, longitude = get_lat_long(user.place_of_birth)
        
        # Create a new user instance
        db_user = User(
            name=user.name,
            email=user.email,
            year=year,
            month=month,
            date=date,
            hours=hours,
            minutes=minutes,
            seconds=seconds,
            latitude=latitude,
            longitude=longitude
        )
        
        # Add and commit the new user to the database
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return db_user

    except IntegrityError as e:
        # Handle database integrity errors (e.g., unique constraint violations)
        db.rollback()  # Rollback the transaction on error
        raise ValueError("An error occurred while creating the user: " + str(e))
    except Exception as e:
        # Handle any other exceptions
        db.rollback()  # Rollback the transaction on error
        raise RuntimeError("An unexpected error occurred: " + str(e))

def update_user(db: Session, user_id: int, user: UserUpdate):
    """Update an existing user in the database."""
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return None
    
    if user.name:
        db_user.name = user.name
    if user.email:
        db_user.email = user.email
    if user.date_of_birth:
        year, month, date = map(int, user.date_of_birth.split('-'))
        db_user.year = year
        db_user.month = month
        db_user.date = date
    if user.time_of_birth:
        hours, minutes, seconds = parse_time(user.time_of_birth)
        db_user.hours = hours
        db_user.minutes = minutes
        db_user.seconds = seconds
    if user.place_of_birth:
        latitude, longitude = get_lat_long(user.place_of_birth)
        db_user.latitude = latitude
        db_user.longitude = longitude
    
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    """Retrieve a user from the database by ID."""
    return db.query(User).filter(User.id == user_id).first()

def delete_user(db: Session, user_id: int):
    """Delete a user from the database by ID."""
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return False
    
    db.delete(db_user)
    db.commit()
    return True
