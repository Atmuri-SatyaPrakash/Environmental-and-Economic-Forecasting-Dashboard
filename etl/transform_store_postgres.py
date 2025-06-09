import psycopg2
from pymongo import MongoClient
from config.config import (
    MONGO_URI, MONGO_DB, MONGO_COLLECTION,
    PG_DB, PG_USER, PG_PASSWORD, PG_HOST
)

def transform():
    try:
        # Connect to MongoDB
        client = MongoClient(MONGO_URI)
        raw_data = client[MONGO_DB][MONGO_COLLECTION]

        # Check if the collection has documents
        if raw_data.count_documents({}) == 0:
            print("⚠️ No documents found in MongoDB collection.")
            return

        # Connect to PostgreSQL
        conn = psycopg2.connect(
            dbname=PG_DB,
            user=PG_USER,
            password=PG_PASSWORD,
            host=PG_HOST
        )
        cur = conn.cursor()

        # Drop existing table if it exists
        cur.execute('DROP TABLE IF EXISTS pm25_data')

        # Create new table
        cur.execute('''
            CREATE TABLE pm25_data (
                datetime_utc TIMESTAMP,
                datetime_local TIMESTAMP,
                value FLOAT,
                latitude FLOAT,
                longitude FLOAT,
                sensors_id INTEGER,
                locations_id INTEGER
            )
        ''')

        inserted = 0

        # Iterate over MongoDB documents and insert into PostgreSQL
        for record in raw_data.find():
            datetime_utc = record.get("datetime", {}).get("utc")
            datetime_local = record.get("datetime", {}).get("local")
            value = record.get("value")
            coordinates = record.get("coordinates", {})
            latitude = coordinates.get("latitude")
            longitude = coordinates.get("longitude")
            sensors_id = record.get("sensorsId")
            locations_id = record.get("locationsId")

            cur.execute('''
                INSERT INTO pm25_data (
                    datetime_utc,
                    datetime_local,
                    value,
                    latitude,
                    longitude,
                    sensors_id,
                    locations_id
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (
                datetime_utc,
                datetime_local,
                value,
                latitude,
                longitude,
                sensors_id,
                locations_id
            ))
            inserted += 1

        # Commit and close connections
        conn.commit()
        cur.close()
        conn.close()
        print(f"✅ Inserted {inserted} rows into PostgreSQL.")

    except Exception as e:
        print(f"❌ ETL error: {e}")

if __name__ == '__main__':
    transform()
