import pymongo
import psycopg2
from config.config import MONGO_URI, PG_DB, PG_HOST, PG_PASSWORD, PG_USER, MONGO_DB
from datetime import datetime

# MongoDB connection
mongo_client = pymongo.MongoClient(MONGO_URI)
mongo_db = mongo_client[MONGO_DB]
mongo_collection = mongo_db["openaq_chennai_measurements"]

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
CREATE TABLE IF NOT EXISTS openaq_measurements (
    id SERIAL PRIMARY KEY,
    sensor_id INTEGER,
    parameter_name TEXT,
    value REAL,
    datetime_from TIMESTAMPTZ,
    datetime_to TIMESTAMPTZ
);
"""
pg_cursor.execute(create_table_query)
pg_conn.commit()

# Extract and Load
inserted_count = 0

for doc in mongo_collection.find():
    try:
        sensor_id = doc.get("sensor_id")
        parameter = doc.get("parameter", {}).get("name")
        value = doc.get("value")
        
        # Parse datetime strings into datetime objects
        datetime_from_str = doc.get("period", {}).get("datetimeFrom", {}).get("utc")
        datetime_to_str = doc.get("period", {}).get("datetimeTo", {}).get("utc")
        
        datetime_from = datetime.strptime(datetime_from_str, "%Y-%m-%dT%H:%M:%SZ") if datetime_from_str else None
        datetime_to = datetime.strptime(datetime_to_str, "%Y-%m-%dT%H:%M:%SZ") if datetime_to_str else None

        insert_query = """
        INSERT INTO openaq_measurements (sensor_id, parameter_name, value, datetime_from, datetime_to)
        VALUES (%s, %s, %s, %s, %s);
        """
        pg_cursor.execute(insert_query, (sensor_id, parameter, value, datetime_from, datetime_to))
        inserted_count += 1
    except Exception as e:
        print(f"Error inserting document: {doc}")
        print(f"Exception: {e}")

pg_conn.commit()
print(f"Total documents inserted: {inserted_count}")

pg_cursor.close()
pg_conn.close()
