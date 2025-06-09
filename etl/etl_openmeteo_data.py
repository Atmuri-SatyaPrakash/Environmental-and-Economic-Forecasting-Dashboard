import pymongo
import psycopg2
from psycopg2 import sql
from datetime import datetime
from config.config import MONGO_URI,PG_DB,PG_HOST,PG_PASSWORD,PG_USER,MONGO_DB
# MongoDB connection
mongo_client = pymongo.MongoClient(MONGO_URI)
mongo_db = mongo_client[MONGO_DB]
mongo_collection = mongo_db["openmeteo_forecast"]

# PostgreSQL connection
pg_conn = psycopg2.connect(
    dbname=PG_DB,
    user=PG_USER,
    password=PG_PASSWORD,
    host=PG_HOST,
    port="5432"
)
pg_cursor = pg_conn.cursor()

# Create table in PostgreSQL
create_table_query = """
CREATE TABLE IF NOT EXISTS openmeteo_forecast (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP,
    temperature REAL,
    humidity REAL,
    wind_speed REAL
);
"""
pg_cursor.execute(create_table_query)
pg_conn.commit()

# Extract and Load
for doc in mongo_collection.find():
    times = doc.get("hourly", {}).get("time", [])
    temperatures = doc.get("hourly", {}).get("temperature_2m", [])
    humidities = doc.get("hourly", {}).get("relative_humidity_2m", [])
    wind_speeds = doc.get("hourly", {}).get("wind_speed_10m", [])

    for i in range(len(times)):
        timestamp = datetime.fromisoformat(times[i])
        temperature = temperatures[i]
        humidity = humidities[i]
        wind_speed = wind_speeds[i]

        insert_query = """
        INSERT INTO openmeteo_forecast (timestamp, temperature, humidity, wind_speed)
        VALUES (%s, %s, %s, %s);
        """
        pg_cursor.execute(insert_query, (timestamp, temperature, humidity, wind_speed))

pg_conn.commit()
pg_cursor.close()
pg_conn.close()
