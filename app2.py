import dash
from dash import dash_table, html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
import random
from datetime import datetime, timedelta

# Set the geographic coordinates for California
lat_min = 32.53
lat_max = 42.01
lon_min = -124.48
lon_max = -114.13

# Set the range for temperature and conductivity
temp_min = 18
temp_max = 21
cond_min = 160
cond_max = 180

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(children=[
                dbc.Container([
                    dbc.Row([
                        dbc.Col([
                            html.H1("Groundwater Well Data Dashboard"),
                        ], width={"size": 8}),
                        dbc.Col([
                            dbc.Button("Generate Sample Data", id='generate_sample_data', color="primary", className="mb-3"),
                                ], style={'margin-top':'10px'}, width={"size": 4}),
                        ])
                ]),
                html.Div(
                    dbc.Row([
                        html.P('Click button to generate two hours of sample temperature and conductivity data for manipulation. Also generates sample coordinates in CA region.')
                    ], style={'margin':'5px'})
                ),
                html.Div(
                    dash_table.DataTable(
                        id='well_data_Table',
                        columns=[
                            {'name':'Well','id':'Well'},
                            {'name':'Latitude','id':'Latitude'},
                            {'name':'Longitude','id':'Longitude'},
                            {'name':'DateTime','id':'DateTime'},
                            {'name':'Temperature (C)','id':'Temperature'},
                            {'name':'Conductivity (microS/cm)','id':'Conductivity'}
                        ],
                        style_table={
                            'overflowX':'scroll',
                            'maxHeight':'300px'
                        }
                    )
                ),
                html.Div(
                    dcc.Graph(
                        id='well_data_Graph'
                        ),
                     style={'width': '100%', 'display': 'inline-block', 'padding': '0 20'})
                
            ])
            
            
            # dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns])
            # ])

# Callback function to generate the sample data when the button is clicked
@app.callback(
    Output(component_id='well_data_Table', component_property='data'),
    Output(component_id='well_data_Graph', component_property='data'),
    [Input(component_id='generate_sample_data', component_property='n_clicks')]
)
def generate_sample_data(n_clicks):
    if n_clicks is None:
        return
    start_date = datetime(2022,1,1,12,0,0)
    data = []
    lat = round(random.uniform(lat_min, lat_max), 4)
    lon = round(random.uniform(lon_min, lon_max), 4)
    for i in range(48):
        date_time = start_date + timedelta(minutes=5*i)  
        temp = round(random.uniform(temp_min, temp_max), 2)
        conductivity = round(random.uniform(cond_min, cond_max), 2)
        data.append(["Well 1", lat, lon, date_time, temp, conductivity])
    df = pd.DataFrame(data, columns=["Well", "Latitude", "Longitude", "DateTime", "Temperature", "Conductivity"])
    return df.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)