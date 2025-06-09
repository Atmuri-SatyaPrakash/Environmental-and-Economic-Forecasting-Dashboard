import requests
from pymongo import MongoClient
from config.config import MONGO_URI, MONGO_DB, OPENAQ_API_KEY,COORDINATES_OPENAQ

# Initialize MongoDB client
client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
collection = db['openaq_chennai_measurements']

# Headers with API Key
headers = {
    "X-API-Key": OPENAQ_API_KEY
}

# Coordinates for Chennai
coordinates = COORDINATES_OPENAQ
radius = 10000  # 10 km radius

def fetch_sensors():
    """
    Fetch sensor IDs for locations within the specified coordinates and radius.
    """
    sensors = []
    # Fetch locations within the specified coordinates and radius
    locations_url = "https://api.openaq.org/v3/locations"
    params = {
        "coordinates": coordinates,
        "radius": radius,
        "limit": 100
    }
    response = requests.get(locations_url, headers=headers, params=params)
    if response.status_code == 200:
        locations_data = response.json()
        for location in locations_data.get("results", []):
            location_id = location.get("id")
            # Fetch sensors for each location
            sensors_url = f"https://api.openaq.org/v3/locations/{location_id}/sensors"
            sensor_response = requests.get(sensors_url, headers=headers)
            if sensor_response.status_code == 200:
                sensor_data = sensor_response.json()
                for sensor in sensor_data.get("results", []):
                    sensor_id = sensor.get("id")
                    sensors.append(sensor_id)
            else:
                print(f"Failed to fetch sensors for location ID {location_id}. Status code: {sensor_response.status_code}")
    else:
        print(f"Failed to fetch locations. Status code: {response.status_code}")
    return sensors

def fetch_and_store():
    """
    Fetch measurements for each sensor and store them in MongoDB.
    """
    sensor_ids = fetch_sensors()
    for sensor_id in sensor_ids:
        measurements_url = f"https://api.openaq.org/v3/sensors/{sensor_id}/measurements"
        params = {
            "limit": 100  # Adjust as needed
        }
        response = requests.get(measurements_url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])
            if results:
                # Add sensor_id to each measurement for reference
                for result in results:
                    result['sensor_id'] = sensor_id
                collection.insert_many(results)
                print(f"✅ Inserted {len(results)} measurements for sensor ID {sensor_id}.")
            else:
                print(f"⚠️ No measurements found for sensor ID {sensor_id}.")
        else:
            print(f"❌ Failed to fetch measurements for sensor ID {sensor_id}. Status code: {response.status_code}")

if __name__ == "__main__":
    fetch_and_store()
