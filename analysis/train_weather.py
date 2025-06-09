# train_weather_model.py
import pandas as pd
from sqlalchemy import create_engine
from statsmodels.tsa.arima.model import ARIMA
from config.config import PG_DB,PG_HOST,PG_PASSWORD,PG_USER
# Load temperature data from PostgreSQL
engine = create_engine(f'postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:5432/{PG_DB}')
df = pd.read_sql("SELECT * FROM openmeteo_forecast", engine)
df['timestamp'] = pd.to_datetime(df['timestamp'])
df.set_index('timestamp', inplace=True)
df = df.asfreq('H')

# Train ARIMA model on temperature_2m
temp_series = df['temperature'].dropna()
model = ARIMA(temp_series, order=(2, 1, 2)).fit()
model.save('models/weather_arima_model.pkl')
print("✅ ARIMA model for temperature saved as 'models/weather_arima_model.pkl'")
