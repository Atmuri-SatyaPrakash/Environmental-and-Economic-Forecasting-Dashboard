import dash
from dash import dcc, html, Input, Output
import pandas as pd
import psycopg2
import plotly.express as px
from config.config import PG_DB, PG_USER, PG_PASSWORD, PG_HOST

def load_data():
    try:
        conn = psycopg2.connect(
            dbname=PG_DB,
            user=PG_USER,
            password=PG_PASSWORD,
            host=PG_HOST
        )
        df = pd.read_sql("SELECT * FROM pm25_data", conn)
        conn.close()
        return df
    except Exception as e:
        print(f"❌ Failed to load data: {e}")
        return pd.DataFrame()

# Load data from PostgreSQL
df = load_data()

# Setup Dash app
app = dash.Dash(__name__)
app.title = "PM2.5 Air Quality Dashboard"

# App layout
app.layout = html.Div([
    html.H2("🌍 PM2.5 Air Quality Dashboard", style={"textAlign": "center"}),

    html.Div([
        html.Label("Select Value Range (µg/m³):"),
        dcc.RangeSlider(
            id='value-slider',
            min=0,
            max=500,
            step=1,
            value=[0, 200],
            marks={i: str(i) for i in range(0, 501, 50)}
        ),
    ], style={'width': '60%', 'padding': '20px'}),

    dcc.Graph(id='map')
])

# Callback to update map
@app.callback(
    Output('map', 'figure'),
    Input('value-slider', 'value')
)
def update_map(selected_range):
    filtered_df = df[
        (df['value'] >= selected_range[0]) &
        (df['value'] <= selected_range[1])
    ]

    if filtered_df.empty:
        fig = px.scatter_geo(title="No data available for selected filter.")
    else:
        fig = px.scatter_geo(
            filtered_df,
            lat='latitude',
            lon='longitude',
            color='value',
            hover_name='locations_id',
            title="PM2.5 Levels (µg/m³)",
            color_continuous_scale='YlOrRd'
        )
        fig.update_layout(geo=dict(showland=True, landcolor="lightgray"))

    return fig

# Run server
if __name__ == '__main__':
    app.run(debug=True)
