# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 15:14:50 2024

@author: Gebruiker
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc


# Initialize the Dash app
app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.SLATE], suppress_callback_exceptions=True)

server = app.server   # required for publishing

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("by Fuel", href="/")),
        dbc.NavItem(dbc.NavLink("by Model", href="/bymodel")),
        dbc.NavItem(dbc.NavLink("by Country", href="/bycountry")),
        html.Div([
            html.Img(src='assets/car_logo.png', height='80vh', style={'float': 'right', 'margin-top': '3px', 'margin-right': '20px'}),
        ], style={'width': '100%'})
    ],
    brand="Car Sales Dashboard",
    color="dark",
    dark=True,
)
 
# Define the layout
app.layout = dbc.Container([
    navbar,
    dash.page_container,  # Placeholder for page content
#    footer, # Placeholder for footer component
], fluid=True)  # Make the container full-width

if __name__ == '__main__':
    app.run(debug=True, port=8031)
    print(dash.page_registry)