# train_gdp_model.py
import joblib
import pandas as pd
from sqlalchemy import create_engine
from sklearn.linear_model import LinearRegression
from config.config import PG_DB,PG_HOST,PG_PASSWORD,PG_USER
# Load temperature data from PostgreSQL
engine = create_engine(f'postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:5432/{PG_DB}')
df = pd.read_sql("SELECT * FROM worldbank_gdp", engine)

# Data preprocessing
df = df[df['value'].notnull()]
df['year'] = df['date'].astype(int)
X = df[['year']]
y = df['value']

# Train model and save
model = LinearRegression()
model.fit(X, y)
joblib.dump(model, 'models/gdp_model.pkl')
print("✅ GDP Linear Regression model saved as 'models/gdp_model.pkl'")
