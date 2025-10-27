"""
Dash app for visualizing light readings from MongoDB.

MongoDB credentials are stored in a separate file `credentials2.py`
"""

# Import libraries
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, callback
import pymongo
from credentials2 import MONGO_URI

# MongoDB Atlas connection
myclient = pymongo.MongoClient(MONGO_URI)
iotdb = myclient['add232iotdb']  # Database name
humidity_data = iotdb["light_readings"]  # Collection name

# Initialize Dash app
app = Dash(__name__)
app.layout = html.Div(
    [
        html.H1('NoSQL Practicals', style={'color': 'blue'}),
        html.H2('Demonstration'),
        html.Div(
            [
                html.H1('Light Reading Graph'),
                dcc.Graph(id="light_graph")
            ]
        ),
        dcc.Interval(
            id='interval-component',
            interval=1 * 1000,  # Update every second
            n_intervals=0
        )
    ]
)

@callback(Output('light_graph', 'figure'), Input('interval-component', 'n_intervals'))
def update_light_fig(n):
    # Fetch data from MongoDB
    data = list(humidity_data.find())
    if not data:
        return px.scatter(title='Light Reading Graph', labels={"x": "Time", "y": "Light Reading"})
    
    # Convert to DataFrame
    data_frame = pd.DataFrame(data)
    
    # Ensure 'time' and 'light_reading' columns are present
    if 'time' not in data_frame.columns or 'light_reading' not in data_frame.columns:
        return px.scatter(title='Light Reading Graph', labels={"x": "Time", "y": "Light Reading"})
    
    # Convert 'time' to datetime format
    data_frame['time'] = pd.to_datetime(data_frame['time'], errors='coerce')

    # Handle cases where 'time' might be NaT (Not a Time) after conversion
    data_frame = data_frame.dropna(subset=['time'])

    # Create the plot
    light_fig = px.scatter(data_frame, x="time", y="light_reading",
                          title='Light Reading Over Time',
                          labels={"time": "Time", "light_reading": "Light Reading"},
                          symbol="light_reading",  # Different symbols for binary values
                          color="light_reading",   # Different colors for binary values
                          color_continuous_scale=px.colors.sequential.Viridis)  # Color scale for binary values

    # Update x-axis to show full range of time data
    light_fig.update_xaxes(title_text='Time', tickformat='%Y-%m-%d %H:%M:%S')
    
    return light_fig

if __name__ == '__main__':
    app.run_server(debug=True)

# open in browser - http://127.0.0.1:8050/
