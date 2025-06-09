from pymongo import MongoClient, errors
from config.config import MONGO_URI, MONGO_DB, MONGO_COLLECTION
from .fetch_data import fetch_latest_pm25
def store_pm25_data(data):
    """
    Stores PM2.5 data into MongoDB.
    """
    if not data:
        print("⚠️ No data to store.")
        return

    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        collection = client[MONGO_DB][MONGO_COLLECTION]

        # Optional: Drop existing data
        collection.drop()

        # Insert new data
        collection.insert_many(data)
        print(f"✅ Inserted {len(data)} records into MongoDB.")
    except errors.PyMongoError as e:
        print(f"❌ MongoDB error: {e}")


if __name__ == "__main__":
    pm25_data = fetch_latest_pm25()
    store_pm25_data(pm25_data)
