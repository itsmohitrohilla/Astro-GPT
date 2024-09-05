from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderQuotaExceeded, GeocoderServiceError
import ssl

# Disable SSL verification for Nominatim (not recommended for production)
try:
    _create_default_https_context = ssl._create_default_https_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = ssl._create_unverified_context

def get_lat_long(place_name):
    # Initialize Nominatim API with a user agent
    geolocator = Nominatim(user_agent="geoapiExercises")
    
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

if __name__ == "__main__":
    place_name = "Pataudi Gurgaon Haryana India"
    latitude, longitude = get_lat_long(place_name)
    
    if latitude is not None and longitude is not None:
        print(f"The latitude and longitude of {place_name} are {latitude}, {longitude}")
    else:
        print("Location not found.")


#/Applications/Python\ 3.11/Install\ Certificates.command
