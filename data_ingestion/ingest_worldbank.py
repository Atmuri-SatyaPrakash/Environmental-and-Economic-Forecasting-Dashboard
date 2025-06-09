import requests
from pymongo import MongoClient
from config.config import MONGO_URI, MONGO_DB,COORDINATES_GDP

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
collection = db['worldbank_gdp']

API_URL = f"https://api.worldbank.org/v2/country/{COORDINATES_GDP}/indicator/NY.GDP.MKTP.CD"
params = {
    "format": "json",
    "per_page": 1000
}

def fetch_and_store():
    response = requests.get(API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        if len(data) > 1:
            records = data[1]
            collection.insert_many(records)
            print(f"✅ Inserted {len(records)} World Bank GDP records.")
        else:
            print("❌ No data found in World Bank response.")
    else:
        print(f"❌ Failed to fetch World Bank data. Status code: {response.status_code}")

if __name__ == "__main__":
    fetch_and_store()
