# dashboard_pm25_anomaly.py
import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import joblib
from sqlalchemy import create_engine

# Load Isolation Forest model
model = joblib.load('models/air_quality_model.pkl')

from config.config import PG_DB,PG_HOST,PG_PASSWORD,PG_USER
engine = create_engine(f'postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:5432/{PG_DB}')
df = pd.read_sql("SELECT * FROM openaq_measurements", engine)
df = df[df['parameter_name'] == 'pm25'].dropna(subset=['value'])
df['anomaly'] = model.predict(df[['value']])
df['datetime'] = pd.to_datetime(df['datetime_from'])

# Setup Dash app
app = dash.Dash(__name__)
app.title = "PM2.5 Anomaly Detection"

app.layout = html.Div([
    html.H2("🌫️ PM2.5 Anomaly Detection Dashboard", style={'textAlign': 'center'}),
    dcc.Graph(id='anomaly-chart')
])

@app.callback(Output('anomaly-chart', 'figure'), Input('anomaly-chart', 'id'))
def update_chart(_):
    fig = px.scatter(
        df,
        x='datetime',
        y='value',
        color=df['anomaly'].map({1: 'Normal', -1: 'Anomaly'}),
        title="PM2.5 Levels with Anomalies",
        labels={'value': 'PM2.5 (µg/m³)', 'datetime': 'Timestamp'},
        color_discrete_map={"Normal": "blue", "Anomaly": "red"}
    )
    return fig

if __name__ == '__main__':
    app.run(debug=True)
