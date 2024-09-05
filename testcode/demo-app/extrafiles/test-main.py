
import requests
import json

url = "https://json.freeastrologyapi.com/d6-chart-info"

payload = json.dumps({
  "year": 2022,
  "month": 8,
  "date": 11,
  "hours": 6,
  "minutes": 0,
  "seconds": 0,
  "latitude": 17.38333,
  "longitude": 78.4666,
  "timezone": 5.5,
  "config": {
    "observation_point": "topocentric",
    "ayanamsha": "lahiri"
  }
})
headers = {
  'Content-Type': 'application/json',
  'x-api-key': 'wyB6CIHea41iFb6l0nEEDaCeW1fFKSm74SVZayOS'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
