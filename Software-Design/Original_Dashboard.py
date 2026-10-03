# Setup the Jupyter version of Dash
from jupyter_dash import JupyterDash

# Configure the necessary Python module imports for dashboard components
import dash_leaflet as dl
from dash import dcc, html
import plotly.express as px
from dash import dash_table
from dash.dependencies import Input, Output, State
import base64
JupyterDash.infer_jupyter_proxy_config()

# Configure OS routines
import os

# Configure the plotting routines
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


#### FIX ME #####
# Match your CRUD Python module file name and class name
from CRUD_Python_Module import AnimalShelter

###########################
# Data Manipulation / Model
###########################
# FIX ME update with your username and password and CRUD Python module name

username = "aacuser"
password = "CS340"
host = 'localhost'
port = 27017
database = 'aac'
collection = 'animals'

# Connect to database via CRUD Module
db = AnimalShelter(username, password, host, port, database, collection)

# class read method must support return of list object and accept projection json input
# sending the read method an empty document requests all documents be returned
df = pd.DataFrame.from_records(db.read({}))

# MongoDB v5+ is going to return the '_id' column and that is going to have an 
# invlaid object type of 'ObjectID' - which will cause the data_table to crash - so we remove
# it in the dataframe here. The df.drop command allows us to drop the column. If we do not set
# inplace=True - it will return a new dataframe that does not contain the dropped column(s)
df.drop(columns=['_id'],inplace=True)

## Debug
# print(len(df.to_dict(orient='records')))
# print(df.columns)


#########################
# Dashboard Layout / View
#########################
app = JupyterDash(__name__)

#FIX ME Add in Grazioso Salvare’s logo
image_filename = 'Grazioso Salvare Logo.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

app.layout = html.Div([
    html.Center([
        html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()), style={'height':'150px'}),
        html.B(html.H1('CS-340 Dashboard - Kristian Sotiri'))
    ]),
    html.Hr(),
    html.Div(
        dcc.RadioItems(
            id='filter-type',
            options=[
                {'label': 'Reset', 'value': 'reset'},
                {'label': 'Water Rescue', 'value': 'water'},
                {'label': 'Mountain/Wilderness Rescue', 'value': 'mountain'},
                {'label': 'Disaster/Individual Tracking', 'value': 'tracking'}
            ],
            value='reset',
            inline=True
        )
    ),
    html.Hr(),
    dash_table.DataTable(id='datatable-id',
                         columns=[{"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns],
                         data=df.to_dict('records'),
        editable = False,
        filter_action = "native",
        sort_action = "native",
        sort_mode = "multi",
        column_selectable = False,
        row_selectable = "single",
        row_deletable = False,
        selected_columns = [],
        selected_rows = [0],
        page_action = "native",
        page_current = 0,
        page_size = 10
    ),
    html.Br(),
    html.Hr(),
    html.Div(className='row',
         style={'display' : 'flex'},
             children=[
        html.Div(
            id='graph-id',
            className='col s12 m6',
            ),
        html.Div(
            id='map-id',
            className='col s12 m6',
            )
        ])
])

#############################################
# Interaction Between Components / Controller
#############################################
@app.callback(Output('datatable-id','data'),
              [Input('filter-type', 'value')])
def update_dashboard(filter_type):
    if filter_type == 'water':
        query = {
            'animal_type': 'Dog',
            'breed': {'$in': ['Labrador Retriever Mix', 'Golden Retriever Mix', 'Newfoundland Mix']},
            'sex_upon_outcome': 'Intact Female',
            'age_upon_outcome_in_weeks': {'$gte': 26, '$lte': 156}
        }
    elif filter_type == 'mountain':
        query = {
            'animal_type': 'Dog',
            'breed': {'$in': ['German Shepherd', 'Alaskan Malamute', 'Old English Sheepdog', 'Siberian Husky', 'Rottweiler']},
            'sex_upon_outcome': 'Intact Male',
            'age_upon_outcome_in_weeks': {'$gte': 26, '$lte': 156}
        }
    elif filter_type == 'tracking':
        query = {
            'animal_type': 'Dog',
            'breed': {'$in': ['Doberman Pinsch', 'German Shepherd', 'Golden Retriever', 'Bloodhound', 'Rottweiler']},
            'sex_upon_outcome': 'Intact Male',
            'age_upon_outcome_in_weeks': {'$gte': 20, '$lte': 300}
        }
    else:
        query = {}

    dff = pd.DataFrame.from_records(db.read(query))
    if '_id' in dff.columns:
        dff.drop(columns=['_id'], inplace=True)
    return dff.to_dict('records')

# Display the breeds of animal based on quantity represented in
# the data table
@app.callback(
    Output('graph-id', "children"),
    [Input('datatable-id', "derived_virtual_data")])
def update_graphs(viewData):
    dff = pd.DataFrame.from_dict(viewData)
    return [
        dcc.Graph(
            figure=px.pie(dff, names='breed', title='Preferred Animals')
        )
    ]
    
#This callback will highlight a cell on the data table when the user selects it
@app.callback(
    Output('datatable-id', 'style_data_conditional'),
    [Input('datatable-id', 'selected_columns')]
)
def update_styles(selected_columns):
    return [{
        'if': { 'column_id': i },
        'background_color': '#D2F3FF'
    } for i in selected_columns]


# This callback will update the geo-location chart for the selected data entry
@app.callback(
    Output('map-id', "children"),
    [Input('datatable-id', "derived_virtual_data"),
     Input('datatable-id', "derived_virtual_selected_rows")])
def update_map(viewData, index):  
    if viewData is None:
        return
    elif index is None:
        return
    
    dff = pd.DataFrame.from_dict(viewData)
    if index is None or len(index) == 0:
        row = 0
    else: 
        row = index[0]
        
    return [
        dl.Map(style={'width': '1000px', 'height': '500px'}, center=[30.75,-97.48], zoom=10, children=[
            dl.TileLayer(id="base-layer-id"),
            dl.Marker(position=[dff.iloc[row,13],dff.iloc[row,14]], children=[
                dl.Tooltip(dff.iloc[row,4]),
                dl.Popup([
                    html.H1("Animal Name"),
                    html.P(dff.iloc[row,8])
                ])
            ])
        ])
    ]

app.run_server()
