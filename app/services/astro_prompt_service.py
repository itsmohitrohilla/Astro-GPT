import requests
import json
from redis import Redis
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models.user_model import User

# Initialize Redis instance
redis_instance = Redis.from_url("redis://localhost", encoding="utf8", decode_responses=True)


def convert_to_description(data: dict) -> str:
    """Convert astrology data into a descriptive format."""
    if 'output' not in data or not data['output']:
        return "No data available"

    astro_data = data['output'][0]
    sign_names = {
        1: "Aries", 2: "Taurus", 3: "Gemini", 4: "Cancer", 5: "Leo",
        6: "Virgo", 7: "Libra", 8: "Scorpio", 9: "Sagittarius",
        10: "Capricorn", 11: "Aquarius", 12: "Pisces"
    }

    descriptions = []

    for item in astro_data.values():
        name = item.get("name")
        full_degree = item.get("fullDegree")
        current_sign = item.get("current_sign")
        is_retro = item.get("isRetro")

        if name is None or full_degree is None or current_sign is None:
            continue

        degree = round(full_degree, 2)
        sign = sign_names.get(current_sign, "Unknown")
        description = f"The {name} is at {degree} degrees in {sign}"

        if is_retro == "true":
            description += " and is retrograde."
        else:
            description += "."

        descriptions.append(description)

    return " ".join(descriptions)

#********************************************************************************

def fetch_astro_info(user_id: int) -> str:
    """Fetch astrology data from the external API based on user information."""
    db = next(get_db())

    try:
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            return {"error": "User not found"}

        payload = json.dumps({
            "year": user.year,
            "month": user.month,
            "date": user.date,
            "hours": user.hours,
            "minutes": user.minutes,
            "seconds": user.seconds,
            "latitude": user.latitude,
            "longitude": user.longitude,
            "timezone": user.timezone,
            "settings": {
                "observation_point": "topocentric",
                "ayanamsha": "lahiri"
            }
        })

        headers = {
            'Content-Type': 'application/json',
            'x-api-key': 'wyB6CIHea41iFb6l0nEEDaCeW1fFKSm74SVZayOS'
        }

        url = "https://json.freeastrologyapi.com/planets"
        response = requests.post(url, headers=headers, data=payload)
        data = response.json()

        if response.status_code == 200:
            return convert_to_description(data)
        else:
            return {"error": f"Failed to fetch data: {response.status_code} - {response.text}"}

    finally:
        db.close()

#********************************************************************************
#main function
def astro_user_report(user_id: int, db: Session = Depends(get_db)) -> dict:
    """
    Retrieve astrology report for the user.
    Check Redis for cached data, if not available fetch from API and update the database.
    Cache the new data in Redis with a 7-day expiry.
    """
    try:
        astro_data = fetch_astro_info(user_id)

        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user.astro_data = astro_data
        db.commit()
        db.refresh(user)

        # Store astro_data in Redis cache (expires in 7 days)
        redis_instance.setex(f"user_{user_id}", 604800, astro_data)

        return(astro_data)

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
