# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 14:18:18 2024

@author: Gebruiker
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dash_table import DataTable, FormatTemplate
from dash.dash_table.Format import Format, Group

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

#helper functions
def format_large_numbers(num):
    if abs(num) >= 1_000_000_000:
        return f'{num / 1_000_000_000:.1f}B'
    elif abs(num) >= 1_000_000:
        return f'{num / 1_000_000:.1f}M'
    elif abs(num) >= 1_000:
        return f'{num / 1_000:.1f}K'
    else:
        return str(num)

def format_change(last_change):
    sign = "+" if last_change > 0 else ""
    triangle = "▲" if last_change > 0 else "▼"
    last_change = round(100 * last_change, 2)
    return f"{triangle}{sign}{last_change}%"




# Load the data
df = pd.read_csv('../car_sales_data.csv', parse_dates=['Date'])
df['Year'] = df.Date.dt.year

yearlist = list(df.Year.unique())[1:]
themelist = ['White_MonoBlue', 'White_MonoYellow', 'Black_Rain', 'Greys_Bright', 'DarkBlue_Orange', 'DarkBlue_Trq']

# Register the page
dash.register_page(__name__)

# Define the layout for the ticker
ticker_layout = html.Div(id='ticker-container', className='ticker-container', children=[
    html.Div(id='ticker', className='ticker', children=[
        html.Div(className='ticker-item', children="Loading...")  # Initial content
    ])
])

# Define the main layout for the page
layout = dbc.Container([
            html.Div([
                dbc.Row([
                ticker_layout,
                dcc.Interval(
                    id='interval-component',
                    interval=60*1000,  # Update every 60 seconds
                    n_intervals=0
                    ),
                ]),
                dbc.Row([                    
                    dbc.Col([
                        html.Div(html.P('Select a Colour Theme'), id='textcolor3-1'),
                        dcc.Dropdown(
                            id = 'colour-dropdown3',
                            options=[{'label': theme, 'value': theme} for theme in themelist],
                            value = 'White_MonoBlue',
                            clearable=False,
                            className='mb-4',
                            ),
                        html.Div(html.P('Select a Previous Year'), id='textcolor3-2'),
                        dcc.Dropdown(
                            id = 'year-dropdown3',
                            options=[{'label': year, 'value': year} for year in yearlist],
                            value = '2023',
                            clearable=False,
                            className='mb-4',
                            ),
                        html.Div(html.P('Select a Country'), id='textcolor3-3'),
                        dcc.Dropdown(
                            id = 'country-dropdown',
                            options=[{'label': model, 'value': model} for model in list(df.Country.unique())],
                            value='France',
                            clearable=False,
                            className='mb-4',
                            ),
                        ], width = 2),
                    dbc.Col([
                        dcc.Graph(
                            figure = helpers.generate_countrymap()
                            )
                        ], width = 6
                        )
                    ]),
                html.Br(),
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            html.H3('Page content to follow'),
                        ], id = 'box3-7'),
                        ], width=4),
                    ]),
                ], id = 'outer-div3',
                ),
            ], fluid=True)



@callback(
    [
        Output('outer-div3', 'style'),
        Output('textcolor3-1', 'style'),
        Output('textcolor3-2', 'style'),
        Output('textcolor3-3', 'style'),
        Output('box3-7', 'style'),
    ],
    [
        Input('colour-dropdown3', 'value'),
        Input('year-dropdown3', 'value'),
        Input('country-dropdown', 'value'),
        Input('interval-component', 'n_intervals')
    ],
    allow_duplicates=True,
)
def update_ticker(selected_theme, selected_year, selected_country, n):
    colors3 = color_schemes[selected_theme]['colors_config']
    cards3 = card_configs[selected_theme]
    year = selected_year

    card_style3 = cards3['card_config']['cardstyle']
    card_title3 = cards3['card_config']['cardtitle'] 
    card_value3 = cards3['card_config']['cardvalue'] 
    
    outer_style3 = {
        'backgroundColor': colors3['colors']['background'],
        'background-image': colors3['colors']['background-image'],
        'padding': '5px'
    }
    text_color3 = {
        'color': colors3['colors']['text']
    }

    dfcountry = df[df.Country == selected_country]

    


    return outer_style3, text_color3, text_color3, text_color3, card_style3      

