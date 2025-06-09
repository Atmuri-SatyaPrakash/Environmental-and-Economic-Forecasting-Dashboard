# import requests
# from pymongo import MongoClient
# from config.config import MONGO_URI, MONGO_DB
# from datetime import datetime, timedelta

# client = MongoClient(MONGO_URI)
# db = client[MONGO_DB]
# collection = db['openmeteo_forecast']

# latitude = 13.0827  # Chennai
# longitude = 80.2707
# start_date = datetime.today().strftime('%Y-%m-%d')
# end_date = (datetime.today() + timedelta(days=7)).strftime('%Y-%m-%d')

# API_URL = "https://api.open-meteo.com/v1/forecast"
# params = {
#     "latitude": latitude,
#     "longitude": longitude,
#     "start_date": start_date,
#     "end_date": end_date,
#     "hourly": "temperature_2m,relative_humidity_2m,wind_speed_10m",
#     "timezone": "Asia/Kolkata"
# }

# def fetch_and_store():
#     response = requests.get(API_URL, params=params)
#     if response.status_code == 200:
#         data = response.json()
#         collection.insert_one(data)
#         print("✅ Open-Meteo forecast data inserted.")
#     else:
#         print(f"❌ Failed to fetch Open-Meteo data. Status code: {response.status_code}")

# if __name__ == "__main__":
#     fetch_and_store()

import requests
from pymongo import MongoClient
from datetime import datetime, timedelta
from config.config import MONGO_URI, MONGO_DB,COORDINATES_OPENAQ

# Initialize MongoDB client
client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
collection = db['openmeteo_forecast']

latitude,longitude = COORDINATES_OPENAQ.split(",")



# Define date range
start_date = datetime.today().strftime('%Y-%m-%d')
end_date = (datetime.today() + timedelta(days=7)).strftime('%Y-%m-%d')

# Open-Meteo API endpoint
API_URL = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": latitude,
    "longitude": longitude,
    "start_date": start_date,
    "end_date": end_date,
    "hourly": "temperature_2m,relative_humidity_2m,wind_speed_10m",
    "timezone": "Asia/Kolkata"
}

def fetch_and_store():
    response = requests.get(API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        collection.insert_one(data)
        print("✅ Open-Meteo forecast data inserted.")
    else:
        print(f"❌ Failed to fetch Open-Meteo data. Status code: {response.status_code}, {response.text}")

if __name__ == "__main__":
    fetch_and_store()

