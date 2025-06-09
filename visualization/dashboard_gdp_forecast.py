import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.graph_objs as go
import joblib
from sqlalchemy import create_engine
import numpy as np

# Load model
model = joblib.load('models/gdp_model.pkl')

from config.config import PG_DB,PG_HOST,PG_PASSWORD,PG_USER
engine = create_engine(f'postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:5432/{PG_DB}')
df = pd.read_sql("SELECT * FROM worldbank_gdp", engine)
df = df[df['value'].notnull()]
df['year'] = df['date'].astype(int)

# Predict next 5 years
last_year = df['year'].max()
future_years = pd.DataFrame({'year': np.arange(last_year + 1, last_year + 6)})
predicted = model.predict(future_years)

# Setup Dash app
app = dash.Dash(__name__)
app.title = "GDP Forecast Dashboard"

app.layout = html.Div([
    html.H2("📈 India GDP Forecast Dashboard", style={'textAlign': 'center'}),
    dcc.Graph(id='gdp-forecast')
])

@app.callback(Output('gdp-forecast', 'figure'), Input('gdp-forecast', 'id'))
def update_chart(_):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['year'], y=df['value'], mode='lines+markers', name='Actual GDP'))
    fig.add_trace(go.Scatter(x=future_years['year'], y=predicted, mode='lines+markers', name='Forecasted GDP'))
    fig.update_layout(title='India GDP Forecast (Next 5 Years)', xaxis_title='Year', yaxis_title='GDP (USD)')
    return fig

if __name__ == '__main__':
    app.run(debug=True)
