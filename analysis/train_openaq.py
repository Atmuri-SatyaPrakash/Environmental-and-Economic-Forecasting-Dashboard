# train_air_model.py
import joblib
import pandas as pd
from sqlalchemy import create_engine
from sklearn.ensemble import IsolationForest

from config.config import PG_DB,PG_HOST,PG_PASSWORD,PG_USER
# Load temperature data from PostgreSQL
engine = create_engine(f'postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:5432/{PG_DB}')
df = pd.read_sql("SELECT * FROM openaq_measurements", engine)
df = df[df['parameter_name'] == 'pm25'].dropna(subset=['value'])

# Train Isolation Forest model
df['value'] = df['value'].fillna(0)
model = IsolationForest(contamination=0.05, random_state=42)
model.fit(df[['value']])
joblib.dump(model, 'models/air_quality_model.pkl')
print("✅ PM2.5 Isolation Forest model saved as 'models/air_quality_model.pkl'")
