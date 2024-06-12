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


# Load the data
df = pd.read_csv('../car_sales_data.csv', parse_dates=['Date'])
df['Year'] = df.Date.dt.year

yearlist = list(df.Year.unique())[1:]
themelist = ['White_MonoBlue', 'White_MonoYellow', 'Black_Rain', 'Greys_Bright', 'DarkBlue_Orange', 'DarkBlue_Trq']
table2_columns = ['Quarter','Q1', 'Q2', 'Q3', 'Q4']

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
                html.Hr(),
                dbc.Row([                    
                    dbc.Col([
                        html.Div(html.P('Select a Colour Theme'), id='textcolor2-1'),
                        dcc.Dropdown(
                            id = 'colour-dropdown2',
                            options=[{'label': theme, 'value': theme} for theme in themelist],
                            value = 'DarkBlue_Orange',
                            clearable=False,
                            className='mb-4',
                            ),
                        html.Div(html.P('Select a Previous Year'), id='textcolor2-2'),
                        dcc.Dropdown(
                            id = 'year-dropdown2',
                            options=[{'label': year, 'value': year} for year in yearlist],
                            value = '2023',
                            clearable=False,
                            className='mb-4',
                            ),
                        html.Div(html.P('Select a Model'), id='textcolor2-3'),
                        dcc.Dropdown(
                            id = 'model-dropdown',
                            options=[{'label': model, 'value': model} for model in list(df.Model.unique())],
                            value='Model_1',
                            clearable=False,
                            className='mb-4',
                            ),
                        ], width = 2),
                    dbc.Col([
                        html.Div([
                        dcc.Graph(
                            id='barline-fig2',
                            figure = {},
                            style = {'height':'40vh'},
                            )
                        ], id = 'box2-1'),                        
                        ], width=4),
                    dbc.Col([
                        html.Div([
                        dcc.Graph(
                            id='dualgauge-2',
                            figure = {},
                            style = {'height':'40vh'},
                            ),
                        ], id = 'box2-2'),                             
                        ], width=2),
                    dbc.Col([
                        html.Div([
                        dcc.Graph(
                            id='bar-fig2-1',
                            figure = {},
                            style = {'height':'40vh'},
                            )
                        ], id = 'box2-3'),
                        ], width=2),
                    dbc.Col([
                        html.Div([
                        dcc.Graph(
                            id='bar-fig2-2',
                            figure = {},
                            style = {'height':'40vh'},
                            )
                        ], id = 'box2-4'),                        
                        ], width=2)
                    ]),
                html.Br(),
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                        html.Img(src='assets/car1.png', style={'margin-top': '3px', 'margin-right': '20px'}),
                        ], id = 'box2-5', style={'height':'30rem'}),                        
                        ],
                        width=2),
                    dbc.Col([
                        dbc.Card([
                        html.Div([html.H5("Quarterly Financial Data", style={'text-align': 'center'}),
                                ],
                                 id='textcolor2-4'),
                        dash_table.DataTable(
                            id='table2',
                            data = helpers.generate_table_df(df, 2023, 'Model_1').to_dict('records'),
                            columns=[{'name': col, 'id': col} for col in table2_columns],
                            style_header= {'backgroundColor': '#ffffff', 'fontWeight': 'bold'},
                            style_table = {'borderRadius': '10px', 'border':'4px solid #ddd'},
                            style_cell = {
                                'color': '#000000',
                                'font-family':'sans-serif',
                                },
                            style_cell_conditional=[
                                {
                                    'if': {'column_id': 'Quarter'},
                                    'textAlign': 'left'
                                },],
                            ),
                        ], id = 'box2-6', style={'height':'30rem'}),
                        ], width = 6),
                    dbc.Col([
                        html.Div([
                        dcc.Graph(
                            id='scatter2',
                            figure = {},
                            style = {'height':'30vh'},
                            )
                        ], id = 'box2-7'),
                        ], width=4),
                    ]),
                ], id = 'outer-div2',
                ),
            ], fluid=True)


@callback(
    [
        Output('outer-div2', 'style'),
        Output('textcolor2-1', 'style'),
        Output('textcolor2-2', 'style'),
        Output('textcolor2-3', 'style'),
        Output('textcolor2-4', 'style'),
        Output('textcolor2-4', 'children'),
        Output('ticker', 'children'),
        Output('barline-fig2', 'figure'),
        Output('dualgauge-2', 'figure'),
        Output('bar-fig2-1', 'figure'),
        Output('bar-fig2-2', 'figure'),
        Output('table2', 'data'),
        Output('table2', 'columns'),
        Output('table2', 'style_header'),
        Output('table2', 'style_cell'),
        Output('scatter2', 'figure'),
        Output('box2-1', 'style'),
        Output('box2-2', 'style'),
        Output('box2-3', 'style'),
        Output('box2-4', 'style'),
        Output('box2-5', 'style'),
        Output('box2-6', 'style'),
        Output('box2-7', 'style'),
    ],
    [
        Input('colour-dropdown2', 'value'),
        Input('year-dropdown2', 'value'),
        Input('model-dropdown', 'value'),
        Input('interval-component', 'n_intervals')
    ],
    allow_duplicates=True,
)
def update_ticker(selected_theme, selected_year, selected_model, n):
    colors = color_schemes[selected_theme]['colors_config']
    cards = card_configs[selected_theme]
    year = selected_year

    card_style = cards['card_config']['cardstyle']
    card_title = cards['card_config']['cardtitle'] 
    card_value = cards['card_config']['cardvalue'] 
    
    table_title = [
        html.H5("Quarterly Financial Data", style={'text-align': 'center'}),
        html.H6(f'{selected_model}   {year}', style={'text-align': 'center'})
        ]
    
    table_style = card_style.copy()
    table_style['height'] = '30vh'

    outer_style = {
        'backgroundColor': colors['colors']['background'],
        'background-image': colors['colors']['background-image'],
        'padding': '5px'
    }
    text_color = {
        'color': colors['colors']['text']
    }

    dfmodel = df[df.Model == selected_model]

    cards = []
    np_value = card_value.copy()
    np_value['color'] = colors['colors']['palet'][1]
    
    for model in list(df.Model.unique()):
        dfM = df[df.Model == model]
        card = dbc.Card(
            dbc.CardBody(
                [
                    html.H6(f'{model}', className='card-title', style=card_title),
                    html.P(f'Cars Sold: {helpers.format_large_numbers(helpers.total_sales_cars(dfM, year))}', className='card-text', style=card_value),
                    html.P(f'Net Profit: {helpers.format_large_numbers(helpers.total_sales_cars(dfM, year))}', className='card-text', style=np_value),
                ]
            ),
            className='ticker-item', style=card_style,
        )
        cards.append(card)

    ticker_children = [
        html.Div(
            children=[dbc.Col(card, className="mb-2", width="auto") for card in cards],
            className='hstack gap-3',
        )
    ]

    dualbarline = helpers.generate_dualbar_line(df, year, colors, selected_model)
    dualgauge = helpers.generate_gauge_multimodel(df, year, 'Profit', colors, selected_model)
    rankmodel = helpers.generate_bars_rankmodel(df, year, colors)
    profitbars = helpers.generate_bars_profitrank(df, year, colors)

    modeltable = helpers.generate_table_df(df, year, selected_model)
    table_columns =[{'name': col, 'id': col} for col in table2_columns]
    
    table_style_header = {
        'backgroundColor': colors['colors']['palet'][1],
        'color': colors['colors']['text'],
        'fontWeight': 'bold'
    }
    
    table_style_cell = {
        'backgroundColor': colors['colors']['bg_figs'],
        'color': colors['colors']['text'],
        'font-family':'sans-serif',
        }

    scatterplot = helpers.generate_scatter_profitvssales(df, colors)

    return outer_style, text_color, text_color, text_color, text_color, table_title, html.Div(className='ticker-item hstack gap-3', children=ticker_children), dualbarline, dualgauge, rankmodel, profitbars, modeltable.to_dict('records'), table_columns, table_style_header, table_style_cell, scatterplot, card_style, card_style, card_style, card_style, card_style, table_style, card_style         

