import pymongo
import psycopg2
from psycopg2 import sql
from config.config import MONGO_URI, PG_DB, PG_HOST, PG_PASSWORD, PG_USER, MONGO_DB
from datetime import datetime

# MongoDB connection
try:
    mongo_client = pymongo.MongoClient(MONGO_URI)
    mongo_db = mongo_client[MONGO_DB]
    mongo_collection = mongo_db["worldbank_gdp"]
    print("✅ Connected to MongoDB.")
except Exception as e:
    print(f"❌ MongoDB connection error: {e}")
    exit(1)

# PostgreSQL connection
try:
    pg_conn = psycopg2.connect(
        dbname=PG_DB,
        user=PG_USER,
        password=PG_PASSWORD,
        host=PG_HOST,
        port="5432"
    )
    pg_cursor = pg_conn.cursor()
    print("✅ Connected to PostgreSQL.")
except Exception as e:
    print(f"❌ PostgreSQL connection error: {e}")
    exit(1)

# Create table in PostgreSQL
create_table_query = """
CREATE TABLE IF NOT EXISTS worldbank_gdp (
    id SERIAL PRIMARY KEY,
    indicator_id TEXT,
    indicator_value TEXT,
    country_id TEXT,
    country_value TEXT,
    countryiso3code TEXT,
    date TEXT,
    value DOUBLE PRECISION,
    unit TEXT,
    obs_status TEXT,
    decimal INTEGER
);
"""

try:
    pg_cursor.execute(create_table_query)
    pg_conn.commit()
    print("✅ PostgreSQL table 'worldbank_gdp' is ready.")
except Exception as e:
    print(f"❌ Error creating table: {e}")
    pg_conn.rollback()
    pg_cursor.close()
    pg_conn.close()
    exit(1)

# Extract and Load
insert_query = """
INSERT INTO worldbank_gdp (
    indicator_id,
    indicator_value,
    country_id,
    country_value,
    countryiso3code,
    date,
    value,
    unit,
    obs_status,
    decimal
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
"""

inserted_count = 0
for doc in mongo_collection.find():
    try:
        indicator_id = doc.get("indicator", {}).get("id")
        indicator_value = doc.get("indicator", {}).get("value")
        country_id = doc.get("country", {}).get("id")
        country_value = doc.get("country", {}).get("value")
        countryiso3code = doc.get("countryiso3code")
        date = doc.get("date")
        value = doc.get("value")
        unit = doc.get("unit")
        obs_status = doc.get("obs_status")
        decimal = doc.get("decimal")

        pg_cursor.execute(insert_query, (
            indicator_id,
            indicator_value,
            country_id,
            country_value,
            countryiso3code,
            date,
            value,
            unit,
            obs_status,
            decimal
        ))
        inserted_count += 1
    except Exception as e:
        print(f"⚠️ Skipping document due to error: {e}")
        continue

pg_conn.commit()
print(f"✅ Inserted {inserted_count} records into 'worldbank_gdp' table.")

# Close connections
pg_cursor.close()
pg_conn.close()
mongo_client.close()
print("✅ ETL process completed successfully.")
