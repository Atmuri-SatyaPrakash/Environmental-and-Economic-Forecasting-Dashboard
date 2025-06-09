# dashboard_weather_forecast.py
import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.graph_objs as go
import joblib
from sqlalchemy import create_engine
from statsmodels.tsa.arima.model import ARIMAResults
from config.config import PG_DB,PG_HOST,PG_PASSWORD,PG_USER

engine = create_engine(f'postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:5432/{PG_DB}')

# Load the ARIMA model
model: ARIMAResults = ARIMAResults.load('models/weather_arima_model.pkl')

# Load actual data from PostgreSQL

df = pd.read_sql("SELECT * FROM openmeteo_forecast", engine)
df['timestamp'] = pd.to_datetime(df['timestamp'])
df.set_index('timestamp', inplace=True)
temp_series = df['temperature'].dropna()

# Forecast next 24 hours
forecast = model.forecast(steps=24)
forecast_index = pd.date_range(start=temp_series.index[-1] + pd.Timedelta(hours=1), periods=24, freq='H')
forecast_series = pd.Series(forecast, index=forecast_index)

# Setup Dash app
app = dash.Dash(__name__)
app.title = "Weather Temperature Forecast"

app.layout = html.Div([
    html.H2("🌦️ Temperature Forecast Dashboard", style={'textAlign': 'center'}),
    dcc.Graph(id='forecast-graph', figure={})
])

@app.callback(Output('forecast-graph', 'figure'), Input('forecast-graph', 'id'))
def display_forecast(_):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=temp_series.index[-100:], y=temp_series[-100:],
                             mode='lines', name='Observed'))
    fig.add_trace(go.Scatter(x=forecast_index, y=forecast_series,
                             mode='lines+markers', name='Forecast'))
    fig.update_layout(title='24-Hour Temperature Forecast', xaxis_title='Time', yaxis_title='Temperature (°C)')
    return fig

if __name__ == '__main__':
    app.run(debug=True)
