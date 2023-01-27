# Groundwater well data dashboard
# imports
# import dash
# from dash import dcc
# from dash import html
# import dash_bootstrap_components as dbc
# from dash.dependencies import Input, Output
# import plotly.express as px
# import pandas as pd
# import geopandas as gpd
# import plotly.graph_objs as go

# # sample data and well location coords
# df = pd.read_csv('groundwater_well_data.csv')
# well_locations = pd.read_csv('well_locations.csv')

# # Create dash app, define layout
# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# app.layout = dbc.Container([
#     dbc.Row([
#         dbc.Col([
#             html.H1('Groundwater Well Data'),
#             dcc.Dropdown(
#                 id='well-selector',
#                 options=[{'label': well, 'value': well} for well in df['well'].unique()],
#                 value='Well 1'
#             ),
#         ]),
#     ]),
#     dbc.Row([
#         dbc.Col([
#             dcc.Graph(id='conductivity-plot'),
#         ]),
#         dbc.Col([
#             dcc.Graph(id='temperature-plot'),
#         ]),
#     ]),
#     dbc.Row([
#         dbc.Col([
#             dcc.Graph(id='map'),
#         ]),
#     ]),
# ])


# # callback to update on newly selected well
# @app.callback(
#     [Output('conductivity-plot', 'figure'), Output('temperature-plot', 'figure')],
#     [Input('well-selector', 'value')]
# )
# def update_plots(selected_well):
#     filtered_df = df[df['well'] == selected_well]
#     conductivity_plot = px.line(filtered_df, x='timestamp', y='conductivity')
#     temperature_plot = px.line(filtered_df, x='timestamp', y='temperature')
#     return conductivity_plot, temperature_plot

# # map update callback
# @app.callback(
#     Output('map', 'figure'),
#     [Input('well-selector', 'value')]
# )
# def update_map(selected_well):
#     filtered_well_locations = well_locations[well_locations['well'] == selected_well]
#     map_figure = px.scatter_mapbox(filtered_well_locations, lat='latitude', lon='longitude')
#     map_figure = map_figure.update_layout(mapbox_style="open-street-map")
#     map_figure = map_figure.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
#     return map_figure

# # run app
# app.run_server(debug=True)

import dash
from dash import html, dash_table
import dash_bootstrap_components as dbc
from dash import dcc
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate
import pandas as pd
import numpy as np
from scipy import stats
import random
from plotly.graph_objs import Scatter, Layout

well_locations = []

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H1("Welcome to Dash"),
            ], width={"size": 12}),
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Button("1. Generate sample temperature data", id='generate_temperature_data', color="primary", className="mb-3"),
            ], width={"size": 4}),
            dbc.Col([
                dbc.Button("2. Generate sample conductivity data", id='generate_conductivity_data', color="primary", className="mb-3"),
            ], width={"size": 4}),
            dbc.Col([
                dbc.Button("3. Generate sample well location", id='generate_well_location', color="primary", className="mb-3"),
            ], width={"size": 4}),
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Button("4. Plot conductivity and temperature time series", id='plot_time_series', color="primary", className="mb-3"),
            ], width={"size": 4}),
            dbc.Col([
                dbc.Button("5. Plot well locations", id='plot_well_locations', color="primary", className="mb-3"),
            ], width={"size": 4}),
            dbc.Col([
                dbc.Button("6. Generate summary statistics", id='generate_summary_stats', color="primary", className="mb-3"),
            ], width={"size": 4}),
        ]),
        html.Div(id='main-content'),
        html.Div(
            dash_table.DataTable(
                id='well_locations_table',
                columns=[
                    {'name':'longitude','id':'lon'},
                    {'name':'latitude','id':'lat'}
                ],
                style_table={
                    'overflowX':'scroll',
                    'maxHeight':'300px'
                }
            )
        ),
        html.Div(
            dbc.Row([
                html.Br()
            ])
        ),
        html.Div([
    # Add a radio button to select which variable to display summary stats for
    dcc.RadioItems(id='var-select',
                  options=[{'label': 'Temperature', 'value': 'temp'},
                           {'label': 'Conductivity', 'value': 'cond'}],
                  value='temp'),
    # Add a button to generate summary statistics
    html.Button('Generate Summary Statistics', id='gen-stats-btn', n_clicks=0),
    # Add a table to display the summary statistics
    dash_table.DataTable(
        id='summary_stats_table',
        data=[],
        columns=[{'name': col, 'id': col} for col in data.columns],
        style_table={
            'overflowX':'scroll',
            'maxHeight':'300px'
        }
        )
    ])
    ])
    ])

df_temp = pd.DataFrame({'time': [], 'Temperature': []})
df_cond = pd.DataFrame({'time': [], 'Conductivity': []})

@app.callback(
    Output('main-content', 'children'),
    [Input('generate_temperature_data', 'n_clicks'),
     Input('generate_conductivity_data', 'n_clicks')])
def generate_conductivity_data(n_clicks_temp, n_clicks_cond):
    if n_clicks_temp is None:
        df_temp = pd.DataFrame({'time': [], 'Temperature': []})
    else:
        df_temp = pd.DataFrame({'time': pd.date_range('2022-01-01', periods=48, freq='5min'),
                               'Temperature': [random.uniform(14,23) for i in range(48)]})
    if n_clicks_cond is None:
        df_cond = pd.DataFrame({'time': [], 'Conductivity': []})
    else:
        df_cond = pd.DataFrame({'time': pd.date_range('2022-01-01', periods=48, freq='5min'),
                               'Conductivity': [random.uniform(168,172) for i in range(48)]})
    data = [Scatter(x=df_temp['time'], y=df_temp['Temperature'], mode='lines', name='Temperature'),
            Scatter(x=df_cond['time'], y=df_cond['Conductivity'], mode='lines', name='Conductivity')]
    layout = Layout(yaxis=dict(title='Temperature (°C)', side='left'),
                   yaxis2=dict(title='Conductivity (µS)', side='right', overlaying='y'))
    return dcc.Graph(figure={'data': data, 'layout': layout})


@app.callback(
    [Output("well_locations_table", "data")],
    [Input("generate_well_location", "n_clicks")],
)
def generate_and_display_well_location(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    else:
        lat = round(random.uniform(32, 42), 6)
        lon = round(random.uniform(-124, -114), 6)
        well_location = [lon,lat]
        return well_location

# callback function to update the table with the summary statistics
@app.callback(
    Output("summary_stats_table", "data"),
    [Input("generate_summary_stats", "n_clicks"),
     Input("variable_selector", "value")],
    [State("temp_data", "data"), State("conductivity_data", "data")],
)
def generate_and_display_summary_stats(n_clicks, variable, temp_data, conductivity_data):
    if n_clicks is None:
        raise PreventUpdate
    else:
        if variable == 'Temperature':
            df = pd.DataFrame(temp_data)
        else:
            df = pd.DataFrame(conductivity_data)

        summary_stats = df.describe()
        summary_stats = summary_stats.rename(columns={'0': variable})
        datadictdf = summary_stats.to_dict('records')
        return datadictdf





if __name__ == '__main__':
    app.run_server(debug=True)