import requests
import json
from app.database.db import get_db
from sqlalchemy.orm import Session
from app.models.user_model import User


def generate_pre_prompt(data):
    # Extracting input data from the provided astrological JSON data
    year = data['input']['year']
    month = data['input']['month']
    date = data['input']['date']
    hours = data['input']['hours']
    minutes = data['input']['minutes']
    seconds = data['input']['seconds']
    latitude = data['input']['latitude']
    longitude = data['input']['longitude']
    timezone = data['input']['timezone']
    observation_point = data['input']['config']['observation_point']
    ayanamsha = data['input']['config']['ayanamsha']
    
    # Prepare planet data from the astrological output
    planets = data['output'][0]

    # Define pre-prompt
    pre_prompt = f"""
    You are a highly knowledgeable astrologer with expertise in interpreting detailed astrological charts. 
    You have access to the user's precise astrological data and are equipped to provide accurate, professional,
    and insightful predictions based on this information.

    The astrological chart for the user is calculated with the following details:
    - Date of Birth: {year}-{month}-{date}
    - Time of Birth: {hours}:{minutes}:{seconds} (Timezone: {timezone} GMT)
    - Location: Latitude {latitude}, Longitude {longitude}
    - Ayanamsa: {ayanamsha}
    - Observation Point: {observation_point}

    Key planetary positions are:
    """
    
    # Adding planetary details
    for idx, planet_data in planets.items():
        planet_name = planet_data['name']
        full_degree = planet_data['fullDegree']
        norm_degree = planet_data['normDegree']
        current_sign = planet_data['current_sign']
        is_retrograde = "Retrograde" if planet_data['isRetro'] == 'true' else "Direct"
        
        pre_prompt += f"\n- **{planet_name}**: {full_degree}° (normalized: {norm_degree}°) in sign {current_sign}, Status: {is_retrograde}"

    pre_prompt += """
    
    When responding to user queries, utilize the following guidelines:
    - Interpret planetary positions and their retrograde statuses with precision.
    - Analyze the impact of each planet's placement on the user's life and current circumstances.
    - Offer detailed insights, predictions, and guidance based on the precise astrological chart provided.
    - Ensure all responses are informed by the user's astrological data to maintain accuracy and relevance.
    
    Structure your response in the following manner:
    - Past**: Address past challenges and difficulties faced by the user based on the astrological chart. Highlight key planetary influences and their historical impact.
    - Present**: Describe the current situation of the user, referencing relevant planetary positions and aspects. Explain ongoing influences and their implications for the present moment.
    - Solution**: Provide guidance on how to address current issues or challenges. Offer practical solutions and strategies for overcoming obstacles, informed by the astrological insights.
    - Future: Conclude with predictions about the user's future, including potential opportunities and trends. Explain how the current planetary influences might shape future developments.
    
    When providing astrological insights:
    - Analyze each planet's position and retrograde status with precision.
    - Address past challenges, current situations, and future predictions based on the chart.
    - Offer concise, practical advice for resolving issues and improving the user's situation.

    Focus on delivering accurate, actionable advice based on the specific astrological details provided.
    Your goal is to provide professional, well-informed, and actionable astrological advice, grounded in the specific details of the user's chart.
    
    """

    return pre_prompt


def fetch_astro_info(user_id: int):
    # Use get_db to create a database session
    db = next(get_db())
    
    try:
        # Fetch user details from the database
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            return {"error": "User not found"}
        
        # Extract user information
        year = user.year
        month = user.month
        date = user.date
        hours = user.hours
        minutes = user.minutes
        seconds = user.seconds
        latitude = user.latitude
        longitude = user.longitude
        timezone = user.timezone

        # Prepare the payload for the API request
        payload = json.dumps({
            "year": year,
            "month": month,
            "date": date,
            "hours": hours,
            "minutes": minutes,
            "seconds": seconds,
            "latitude": latitude,
            "longitude": longitude,
            "timezone": timezone,
            "settings": {
                "observation_point": "topocentric",
                "ayanamsha": "lahiri"
            }
        })

        headers = {
            'Content-Type': 'application/json',
            'x-api-key': 'wyB6CIHea41iFb6l0nEEDaCeW1fFKSm74SVZayOS'  
        }

        # Send the request to the astrology API
        url = "https://json.freeastrologyapi.com/planets"
        response = requests.post(url, headers=headers, data=payload)
        data = response.json()
        
        # Check if the response is successful
        if response.status_code == 200:
            return generate_pre_prompt(data) # Return JSON data from the response
        else:
            return {"error": f"Failed to fetch data: {response.status_code} - {response.text}"}
    
    finally:
        # Close the session
        db.close()
