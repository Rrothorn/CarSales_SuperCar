import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Input, Output

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

from config import color_schemes, card_configs
import helpers

import pandas as pd
import numpy as np
import datetime

    
# Load the data
df = pd.read_csv('../car_sales_data.csv', parse_dates=['Date'])
df['Year'] = df.Date.dt.year

yearlist = list(df.Year.unique())[1:]
themelist = ['White_MonoBlue', 'White_MonoYellow', 'Black_Rain', 'Greys_Bright', 'DarkBlue_Orange', 'DarkBlue_Trq']

# Initialize the Dash app
dash.register_page(__name__, path='/')

# Layout of the dashboard
layout = dbc.Container([
    html.Div([
    dbc.Row([   # first Row for info cards
        dbc.Col([
        html.Div(
            id = 'card-contents',
            children=[
                dbc.Card(id='card-1', body=True, className='w-100'),                
                dbc.Card(id='card-2', body=True, className='w-100'),
                dbc.Card(id='card-3', body=True, className='w-100'),
                dbc.Card(id='card-4', body=True, className='w-100'),
                ],
            className = 'hstack gap-3',
            ),
        ], width=7),
        dbc.Col([
        html.Div(html.P('Select a Previous Year'), id='textcolor-1'),
            dcc.Dropdown(
                id = 'year-dropdown',
                options=[{'label': year, 'value': year} for year in yearlist],
                value = '2023',
                clearable=False,
                className='mb-4',
                )
            ], width = 2),  
        dbc.Col(width = 1),
        dbc.Col([
        html.Div(html.P('Select a Colour Theme'), id='textcolor-2'),
            dcc.Dropdown(
                id = 'colour-dropdown',
                options=[{'label': theme, 'value': theme} for theme in themelist],
                value = 'White_MonoBlue',
                clearable=False,
                className='mb-4',
                )
            ], width = 2),
        ]),
    html.Br(),
    dbc.Row([
        dbc.Col([
            html.Div([            
            dcc.Graph(id='fuelsource_donut',
                      figure = {},
                      style={'height':'44vh'},
                      )
            ], id = 'box-1',
            ),  
        ], width=2),
        dbc.Col([
            html.Div([
            dcc.Graph(id='fuelyoy_gauge',
                      style = {'height':'44vh'},
                      )  
                ], id = 'box-2',
                ),                
              ], width = 5),
        dbc.Col([
            html.Div([
            dcc.Graph(id='fuelqoq_bar',
                      style = {'height':'44vh'}
                      )
                        ], id = 'box-3',
                        ),             
              ], width = 5),
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col([
            html.Div([
            dcc.Graph(id='country_fuel_bar',
                      figure = {},
                      style = {'height':'40vh'}
                      )
                ], id = 'box-4',
                ), 
        ], width=7),
        dbc.Col([
            html.Div([
            dcc.Graph(id='heatmap',
                      figure = {},
                      style = {'height':'40vh'}
                      )
                ], id = 'box-5',
                ), 
        ], width=5),

    ]),
    ], id = 'outer-div',
       style = {}
    ),
], fluid=True)


# Callback to update store sales trend graph
@callback(
    [
    Output('outer-div', 'style'),
    Output('textcolor-1', 'style'),
    Output('textcolor-2', 'style'),
    Output('card-1', 'style'),
    Output('card-1', 'children'),
    Output('card-2', 'style'),
    Output('card-2', 'children'),
    Output('card-3', 'style'),
    Output('card-3', 'children'),
    Output('card-4', 'style'),
    Output('card-4', 'children'),  
    Output('box-1', 'style'),
    Output('box-2', 'style'),
    Output('box-3', 'style'),
    Output('box-4', 'style'),
    Output('box-5', 'style'),
    Output('fuelsource_donut', 'figure'),
    Output('fuelyoy_gauge', 'figure'),
    Output('fuelqoq_bar', 'figure'),
    Output('country_fuel_bar', 'figure'),
    Output('heatmap', 'figure')
    ],
    [
    Input('year-dropdown', 'value'),
    Input('colour-dropdown', 'value'),
    ],
    allow_duplicates=True,
)

def update_byFuel(selected_year, selected_colour):
    year = int(selected_year)
    colors = color_schemes[selected_colour]['colors_config']
    cards = card_configs[selected_colour]
    
    outer_style = {
            'backgroundColor': colors['colors']['background'],
            'background-image': colors['colors']['background-image'],
            # 'color': colors['text'],
            'padding': '5px'
            }
    
    text_color = {
        'color': colors['colors']['text']
        }
    
    card_style = cards['card_config']['cardstyle']
    card_title = cards['card_config']['cardtitle'] 
    card_value = cards['card_config']['cardvalue'] 
    
    
    card_contents = [
        dbc.CardBody(
            [
            html.H4('SALES', className='card-title', style=card_title),
            html.P(helpers.format_large_numbers(helpers.total_sales_EUR(df, year)), className='card-text', style=card_value),
            ]
            ),
        dbc.CardBody(
            [
            html.H4('CARS SOLD', className='card-title', style=card_title),
            html.P(helpers.format_large_numbers(helpers.total_sales_cars(df, year)), className='card-text', style=card_value),
            ]
            ),        
        dbc.CardBody(
            [
            html.H4('SALES YoY', className='card-title', style=card_title),
            html.P(helpers.total_sales_EUR_yoy(df, year), className='card-text', style=card_value),
            ]
            ),
        dbc.CardBody(
            [
            html.H4('SALES QoQ', className='card-title', style = card_title),
            html.P(helpers.total_sales_EUR_qoq(df, year), className='card-text', style=card_value),
            ]
            ),
        ]
    
    donut = helpers.generate_donut_sales_fuel(year, colors)
    multi_gauge = helpers.generate_gauge_multi(df, year, 'SalesEUR', colors)
    multi_bar = helpers.generate_bars_qoqmulti(df, year, 'SalesEUR', colors)
    barfig = helpers.generate_bars_fuelstacked_country(year, 'SalesEUR', colors)
    trendmap = helpers.create_heatmap(colors)
    return [
        outer_style, text_color, text_color,
        card_style, card_contents[0],
        card_style, card_contents[1],
        card_style, card_contents[2],
        card_style, card_contents[3],
        card_style, card_style, card_style, card_style, card_style,
        donut, multi_gauge, multi_bar, barfig, trendmap
        ]

