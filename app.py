# Groundwater well data dashboard
# imports
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import geopandas as gpd

# sample data and well location coords
df = pd.read_csv('groundwater_well_data.csv')
well_locations = pd.read_csv('well_locations.csv')

# Create dash app, define layout
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1('Groundwater Well Data'),
            dcc.Dropdown(
                id='well-selector',
                options=[{'label': well, 'value': well} for well in df['well'].unique()],
                value='Well 1'
            ),
        ]),
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='conductivity-plot'),
        ]),
        dbc.Col([
            dcc.Graph(id='temperature-plot'),
        ]),
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='map'),
        ]),
    ]),
])


# callback to update on newly selected well
@app.callback(
    [Output('conductivity-plot', 'figure'), Output('temperature-plot', 'figure')],
    [Input('well-selector', 'value')]
)
def update_plots(selected_well):
    filtered_df = df[df['well'] == selected_well]
    conductivity_plot = px.line(filtered_df, x='timestamp', y='conductivity')
    temperature_plot = px.line(filtered_df, x='timestamp', y='temperature')
    return conductivity_plot, temperature_plot

# map update callback
@app.callback(
    Output('map', 'figure'),
    [Input('well-selector', 'value')]
)
def update_map(selected_well):
    filtered_well_locations = well_locations[well_locations['well'] == selected_well]
    map_figure = px.scatter_mapbox(filtered_well_locations, lat='latitude', lon='longitude')
    map_figure = map_figure.update_layout(mapbox_style="open-street-map")
    map_figure = map_figure.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return map_figure

# run app
app.run_server(debug=True)

