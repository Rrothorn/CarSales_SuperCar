# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 12:09:58 2024

@author: Gebruiker
"""
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import dash_bootstrap_components as dbc

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots


#from config import color_schemes, card_configs
#import config

import pandas as pd
import numpy as np
import datetime

# Load the data
df = pd.read_csv('../car_sales_data.csv', parse_dates=['Date'])
df['Year'] = df.Date.dt.year


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

def total_sales_cars(df, year):
    start_date = str(year) + '-01-01'
    end_date = str(year) + '-12-31'
    dfc = df[(df.Date >= start_date) & (df.Date <= end_date)]
    cars = dfc.Sales.sum()
    return cars

def total_sales_EUR(df, year):
    start_date = str(year) + '-01-01'
    end_date = str(year) + '-12-31'
    dfc = df[(df.Date >= start_date) & (df.Date <= end_date)]
    amount = round(dfc.SalesEUR.sum(), 0)
    return amount

def total_sales_cars_yoy(df, year):
    prev_year = year - 1
    sc_prev = total_sales_cars(df, prev_year)
    sc_cur = total_sales_cars(df, year)
    yoy = (sc_cur - sc_prev) / sc_prev
    yoy = "{:.2%}".format(yoy)
    return yoy

def total_sales_EUR_yoy(df, year):
    prev_year = year - 1
    sc_prev = total_sales_EUR(df, prev_year)
    sc_cur = total_sales_EUR(df, year)
    yoy = (sc_cur - sc_prev) / sc_prev
    yoy = "{:.2%}".format(yoy)
    return yoy

def total_sales_EUR_qoq(df, year):
    prev_year = year -1
    dfqoq = calculate_qoq_sales(df, year)
    qoq = (dfqoq[prev_year].iloc[-1] - dfqoq[year].iloc[-1]) / dfqoq[prev_year].iloc[-1]
    qoq = "{:.2%}".format(qoq)
    return qoq

# Function to convert datetime to quarterly string format YYYYQ1
def datetime_to_quarter_str(date):
    year = date.year
    quarter = (date.month - 1) // 3 + 1
    return f'{year}Q{quarter}'

def calculate_qoq_sales(df, year):
    year = int(year)
    prev_year = year -1
    # Convert 'Date' to quarterly periods and then to the format 'YYYYQ1'
    df['Quarter'] = df['Date'].apply(datetime_to_quarter_str)   # Filter the data for the years 2022 and 2023    
    df_filtered = df[df.Year.isin([prev_year, year])]
    
    # Aggregate the sales data by quarter for each year
    sales_by_quarter = df_filtered.groupby(['Quarter', 'Year'])['SalesEUR'].sum().reset_index()
    # Extract year and quarter from the 'Quarter' string
   # sales_by_quarter['Year'] = sales_by_quarter['Quarter'].str[:4].astype(int)
   # sales_by_quarter['Quarter'] = sales_by_quarter['Quarter'].str[4:].astype(str)

    # Pivot the data to have years as columns and quarters as rows
    sales_pivot = sales_by_quarter.pivot(index='Quarter', columns='Year', values='SalesEUR')

    # Calculate the QoQ percentage change for each quarter in 2023 compared to 2022
    sales_pivot['QoQ_Change'] = ((sales_pivot[year] - sales_pivot[prev_year]) / sales_pivot[prev_year])
    # Filter the results to only include the quarters of 2023
    qoq_sales = sales_pivot[['QoQ_Change']].dropna()

    return sales_pivot

def calculate_qoq_cars_sold(df, year):
    year = int(year)
    prev_year = year -1

    # Convert 'Date' to quarterly periods and then to the format 'YYYYQ1'
    df['Quarter'] = df['Date'].apply(datetime_to_quarter_str)   # Filter the data for the years 2022 and 2023    
    df_filtered = df[df.Year.isin([prev_year, year])]
 #   print(df_filtered)
    # Aggregate the sales data by quarter for each year
    sales_by_quarter = df_filtered.groupby(['Quarter', 'Year'])['Sales'].sum().reset_index()
  #  print(sales_by_quarter)
    # Extract year and quarter from the 'Quarter' string
 #   sales_by_quarter['Year'] = sales_by_quarter['Quarter'].str[:4].astype(int)
 #   sales_by_quarter['Quarter'] = sales_by_quarter['Quarter'].str[4:].astype(str)
 #   print(sales_by_quarter)
    # Pivot the data to have years as columns and quarters as rows
    sales_pivot = sales_by_quarter.pivot(index='Quarter', columns='Year', values='Sales')

    # Calculate the QoQ percentage change for each quarter in 2023 compared to 2022
    sales_pivot['QoQ_Change'] = ((sales_pivot[year] - sales_pivot[prev_year]) / sales_pivot[prev_year])
    # Filter the results to only include the quarters of 2023
    qoq_sales = sales_pivot[['QoQ_Change']].dropna()

    return sales_pivot

def generate_donut_sales_fuel(year, colors):
    #data prep for Quarterly and Monthly comparisons / donutchart
    start_date = str(year) + '-01-01'
    end_date = str(year) + '-12-31' 
    col = 'Sales'
    dfc = df[(df.Date >= start_date) & (df.Date <= end_date)]
    
    df_fuel = pd.DataFrame(dfc.groupby(dfc.FuelSource)[col].sum())  
        
    donut = px.pie(
                df_fuel,
                values=col,
                names=df_fuel.index,
                title = f'<b>Cars Sold by FuelSource</b>',
                color_discrete_sequence = colors['colors']['palet'],
                hole=0.4,
                labels = {'tickformat':',.2%'}
                )    
    donut.update_layout(
                        plot_bgcolor= colors['colors']['bg_figs'],
                        paper_bgcolor = colors['colors']['surround_figs'],
                        font_color = colors['colors']['text'],
#                        font_family = colors_config['colors']['font'],
                        margin = {'l':30, 'r':30, 't':80, 'b':0, 'pad':0},
                        title = {'font':{'size':18} },
                        legend = {'title': '', 'orientation':'h', 'y':-0.12, 'xanchor':'left', 'x':0.03},                       
                        showlegend = True,
                        )
    donut.update_traces(#textinfo='label+value',
                        #texttemplate='%{label}: %{value:.2%}',  # Format text as label: percentage
                        hovertemplate='%{label}: %{value:.0f}',  # Format hover text as label: percentage
                        )
    return donut  

def generate_bars_bestmodel(year, selected_sales):
    #data prep for Quarterly and Monthly comparisons / donutchart
    start_date = str(year) + '-01-01'
    end_date = str(year) + '-12-31'   
    dfc = df[(df.Date >= start_date) & (df.Date <= end_date)]
    col = selected_sales

    df_best =   pd.DataFrame(dfc[['Model', 'Sales', 'SalesEUR']].groupby(dfc.Model).sum())  
        
    bars = px.bar(df_best, x=df_best.index, y=col)
    return bars

def generate_gauge_yoytarget_fuel(dfg, year, selected_sales, colors):
    col = selected_sales
    
    #get current and previous years sales
    start_date = str(year) + '-01-01'
    end_date = str(year) + '-12-31'   
    dfc = dfg[(dfg.Date >= start_date) & (dfg.Date <= end_date)]
    cur_sales = dfc[col].sum() 
    
    prev_year = year -1
    start_date = str(prev_year) + '-01-01'
    end_date = str(prev_year) + '-12-31'   
    dfc = dfg[(dfg.Date >= start_date) & (dfg.Date <= end_date)]
    sales_target = dfc[col].sum() 
    
    if cur_sales/sales_target < 0.9:
        bar_color = colors['colors']['palet'][1]
    elif cur_sales/sales_target > 1.1:
        bar_color = colors['colors']['palet'][0]
    else:
        bar_color = colors['colors']['palet'][2]
    
    #create a Gauge Graph 
    fig_target = go.Indicator(
       domain = {'x': [0, 1], 'y': [0, 0.8]},
       value = cur_sales/sales_target,
       number={'valueformat': '.2%'},
       mode = "gauge+number+delta",   # also including the delta to show how far off the target we are
#       title = {'text': f'{figln_title} Sales vs Target'},
       delta = {'reference':  1, 'valueformat': '.2%'},
       gauge = {'axis': {'range': [None, 1.3], 'tickformat':',.2%', 'tickvals':[0,1]},
                'bar': {'color': bar_color},                 
                'steps' : [{'range': [0, 1.3], 'color': '#FFFFFF'},],
                'threshold' : {'line': {'color': colors['colors']['palet'][2], 'width': 4}, 'thickness': 0.75, 'value': 1},
                },
       )

    return fig_target

def generate_gauge_multi(df, year, selected_sales, colors):
    subtitles = [           
                df.FuelSource.unique()[0],
                df.FuelSource.unique()[1],
                df.FuelSource.unique()[2],
                df.FuelSource.unique()[3]
                ]
    # Create a subplot figure with 2x2 layout, specifying the type as 'indicator'
    multi_gauge = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            df.FuelSource.unique()[0],
            df.FuelSource.unique()[1],
            df.FuelSource.unique()[2],
            df.FuelSource.unique()[3]
            ),
        specs=[[{'type': 'indicator'}, {'type': 'indicator'}],
                [{'type': 'indicator'}, {'type': 'indicator'}]],
        vertical_spacing=0.3  # Increase vertical spacing between subplots
    )
    
    # Add gauge plots to the subplots
    for i in range(4):
        row = 1 if i < 2 else 2
        col = i % 2 + 1 
        fuel = df.FuelSource.unique()[i]
        dfg = df[df.FuelSource == fuel]
        gauge = generate_gauge_yoytarget_fuel(dfg, year, 'SalesEUR', colors)
        multi_gauge.add_trace(gauge, row=row, col=col)
    # Update layout to add a main title
    multi_gauge.update_layout(
        plot_bgcolor= colors['colors']['bg_figs'],
        paper_bgcolor = colors['colors']['surround_figs'],
        font_color = colors['colors']['text'],
        title_text="<b>Sales Target YoY</b>",
        title_x=0.5,  # Center the main title
        title_font=dict(
 #           family="Arial",  # Specify the font family
            size=18,         # Specify the font size
            color= colors['colors']['text'],     # Specify the font color
            ),
        margin=dict(t=80)  # Adjust the top margin to make room for the main title
    )    
    return multi_gauge

def generate_gauge_yoytarget_model(dfg, year, selected_sales, colors, model):
    col = selected_sales
    
    #get current and previous years sales
    start_date = str(year) + '-01-01'
    end_date = str(year) + '-12-31'   
    dfc = dfg[(dfg.Date >= start_date) & (dfg.Date <= end_date)]
    dfc = dfc[dfc.Model == model]
    cur_profit = dfc[col].sum() 
    
    year = int(year)
    prev_year = year -1
    start_date = str(prev_year) + '-01-01'
    end_date = str(prev_year) + '-12-31'   
    dfc = dfg[(dfg.Date >= start_date) & (dfg.Date <= end_date)]
    dfc = dfc[dfc.Model == model]
    profit_target = dfc[col].sum() 
    
    if cur_profit/profit_target < 0.9:
        bar_color = colors['colors']['palet'][1]
    elif cur_profit/profit_target > 1.1:
        bar_color = colors['colors']['palet'][0]
    else:
        bar_color = colors['colors']['palet'][2]
    
    #create a Gauge Graph 
    fig_target = go.Indicator(
       domain = {'x': [0, 1], 'y': [0, 0.8]},
       value = cur_profit/profit_target,
       number={'valueformat': '.2%'},
       mode = "gauge+number+delta",   # also including the delta to show how far off the target we are
#       title = {'text': f'{figln_title} Sales vs Target'},
       delta = {'reference':  1, 'valueformat': '.2%'},
       gauge = {'axis': {'range': [None, 1.3], 'tickformat':',.2%', 'tickvals':[0,1]},
                'bar': {'color': bar_color},  
        #        'shape':'angular',
                'steps' : [{'range': [0, 1.3], 'color': '#FFFFFF'},],
                'threshold' : {'line': {'color': colors['colors']['palet'][2], 'width': 4}, 'thickness': 0.75, 'value': 1},
                },
       )
  

    return fig_target

def generate_gauge_qoqtarget_model(dfg, year, selected_sales, colors, model):
    col = selected_sales
    
    #get current and previous years sales
    start_date = str(year) + '-09-30'
    end_date = str(year) + '-12-31'   
    dfc = dfg[(dfg.Date >= start_date) & (dfg.Date <= end_date)]
    dfc = dfc[dfc.Model == model]
    cur_profit = dfc[col].sum() 
    
    year = int(year)
    prev_year = year -1
    start_date = str(prev_year) + '-09-30'
    end_date = str(prev_year) + '-12-31'   
    dfc = dfg[(dfg.Date >= start_date) & (dfg.Date <= end_date)]
    dfc = dfc[dfc.Model == model]
    profit_target = dfc[col].sum() 
    
    if cur_profit/profit_target < 0.9:
        bar_color = colors['colors']['palet'][1]
    elif cur_profit/profit_target > 1.1:
        bar_color = colors['colors']['palet'][0]
    else:
        bar_color = colors['colors']['palet'][2]
    
    #create a Gauge Graph 
    fig_target = go.Indicator(
       domain = {'x': [0, 1], 'y': [0, 0.8]},
       value = cur_profit/profit_target,
       number={'valueformat': '.2%'},
       mode = "gauge+number+delta",   # also including the delta to show how far off the target we are
#       title = {'text': f'{figln_title} Sales vs Target'},
       delta = {'reference':  1, 'valueformat': '.2%'},
       gauge = {'axis': {'range': [None, 1.3], 'tickformat':',.2%', 'tickvals':[0,1]},
                'bar': {'color': bar_color},  
        #        'shape':'angular',
                'steps' : [{'range': [0, 1.3], 'color': '#FFFFFF'},],
                'threshold' : {'line': {'color': colors['colors']['palet'][2], 'width': 4}, 'thickness': 0.75, 'value': 1},
                },
       )
  

    return fig_target

def generate_gauge_multimodel(df, year, selected_sales, colors, model):
    subtitles = [           
                'Net Profit QoQ',
                'Net Profit YoY',
                ]
    # Create a subplot figure with 2x2 layout, specifying the type as 'indicator'
    multi_gauge = make_subplots(
        rows=2, cols=1,
        subplot_titles=(
            subtitles
            ),
        specs=[[{'type': 'indicator'}],
                [{'type': 'indicator'}]],
        vertical_spacing=0.3  # Increase vertical spacing between subplots
    )
    
    # Add gauge plots to the subplots
    for i in range(2):
        row = i+1
        col = 1 
        if row == 1:
            gauge = generate_gauge_qoqtarget_model(df, year, 'Profit', colors, model)
        else:
            gauge = generate_gauge_yoytarget_model(df, year, 'Profit', colors, model)
        multi_gauge.add_trace(gauge, row=row, col=col)
    # Update layout to add a main title
    multi_gauge.update_layout(
        plot_bgcolor= colors['colors']['bg_figs'],
        paper_bgcolor = colors['colors']['surround_figs'],
        font_color = colors['colors']['text'],
        title_text=f"<b>{model} Targets {year}</b>",
        title_x=0.5,  # Center the main title
        title_font=dict(
 #           family="Arial",  # Specify the font family
            size=18,         # Specify the font size
            color= colors['colors']['text'],     # Specify the font color
            ),
        margin=dict(t=80)  # Adjust the top margin to make room for the main title
    )    
    return multi_gauge


def generate_bars_qoq(dff, year, selected_sales, colors):
    prev_year = year -1
    col = selected_sales
    
    colors = colors['colors']['palet']
    df_qoq = calculate_qoq_sales(dff, year)
    df_qoq = df_qoq[[prev_year, year]]
    figbar = go.Figure()
    for i, col in enumerate(df_qoq.columns):
        figbar.add_trace(go.Bar(
            name=str(col),
            x=df_qoq.index,
            y=df_qoq[col],
            marker_color=colors[i % len(colors)]  # Set color for each bar
        ))
    
    figbar.update_layout(barmode='group')    
    return figbar

def generate_bars_qoqmulti(df, year, selected_sales, colors):
    # Create a subplot figure with 2x2 layout, specifying the type as 'xy' for bar charts
    multi_bars = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            df.FuelSource.unique()[0],
            df.FuelSource.unique()[1],
            df.FuelSource.unique()[2],
            df.FuelSource.unique()[3]
        ),
        specs=[[{'type': 'xy'}, {'type': 'xy'}],
               [{'type': 'xy'}, {'type': 'xy'}]],
        vertical_spacing=0.3  # Increase vertical spacing between subplots
    )
    
    # Add bar plots to the subplots
    for i in range(4):
        row = 1 if i < 2 else 2
        col = i % 2 + 1 
        fuel = df.FuelSource.unique()[i]
        dfg = df[df.FuelSource == fuel]
        barfig = generate_bars_qoq(dfg, year, selected_sales, colors)
        for trace in barfig.data:
            multi_bars.add_trace(trace, row=row, col=col)

    # Update layout to add a main title
    multi_bars.update_layout(
        plot_bgcolor= colors['colors']['bg_figs'],
        paper_bgcolor = colors['colors']['surround_figs'],
        font_color = colors['colors']['text'],
        title_text="<b>Sales Target QoQ</b>",
        title_x=0.5,  # Center the main title
        margin=dict(t=80),  # Adjust the top margin to make room for the main title
        title_font=dict(
     #       family="Arial",  # Specify the font family
            size=18,         # Specify the font size
            color=colors['colors']['text'],  # Specify the font color
    ),
    )
    
    return multi_bars   

def generate_bars_fuelstacked_country(year, selected_sales, colors):
    #data prep for Quarterly and Monthly comparisons / donutchart
    start_date = str(year) + '-01-01'
    end_date = str(year) + '-12-31'   
    dfc = df[(df.Date >= start_date) & (df.Date <= end_date)]
    col = selected_sales
    
    # Group the data by Country and FuelSource and sum the Sales
    grouped = df.groupby(['Country', 'FuelSource'])['SalesEUR'].sum().reset_index()

    # Pivot the data
    df_country = grouped.pivot(index='Country', columns='FuelSource', values='SalesEUR').fillna(0)
    
    figbar = px.bar(df_country, x=df_country.index, y=df_country.columns,
                    title = '<b>Sales per Country and FuelSource</b>',
                    color_discrete_sequence = colors['colors']['palet']
                    )
    figbar.update_layout(
                        plot_bgcolor= colors['colors']['bg_figs'],
                        paper_bgcolor = colors['colors']['surround_figs'],
                        font_color = colors['colors']['text'],
#                        font_family = colors_config['colors']['font'],
                        margin = {'l':30, 'r':30, 't':80, 'b':0, 'pad':0},
                        title = {'font':{'size':18},
                                 'x':0.5,
                                 },
                        )
    return figbar
    

def create_heatmap(colors):

    # Extract year as an integer
    df['Year'] = df['Date'].dt.year.astype(int)
    # Aggregate data to ensure no duplicate values
    df_agg = df.groupby(['FuelSource', 'Year'])['Sales'].sum().reset_index()
    heatmap_data = df_agg.pivot(index='FuelSource', columns='Year', values='Sales')

    # Create a heatmap
    fig = px.imshow(heatmap_data, labels=dict(x="Year", y="FuelSource", color="Sales"),
                    title="<b>YoY Car Sales Trend by Fuel Source</b>",  color_continuous_scale= colors['colors']['heatmap'])
    fig.update_layout(
                        plot_bgcolor= colors['colors']['bg_figs'],
                        paper_bgcolor = colors['colors']['surround_figs'],
                        font_color = colors['colors']['text'],
#                        font_family = colors_config['colors']['font'],
                        margin = {'l':30, 'r':30, 't':80, 'b':0, 'pad':0},
                        title = {'font':{'size':18},
                                 'x':0.5,
                                 },
                        )    
    return fig

def generate_countrymap():
    
    df_country = pd.DataFrame(df[['Country', 'Sales', 'SalesEUR']].groupby(df.Country).sum())      # Create the choropleth map
    df_country.Country = df_country.index
    fig = px.choropleth(
        df_country,
        locations='Country',
        locationmode='country names',
        color='SalesEUR',
        hover_name='Country',
        hover_data=['SalesEUR'],
        color_continuous_scale=px.colors.sequential.deep,
        title='Car Sales in Europe'
    )
    fig.update_geos(
        scope='europe',
        showcountries=True,
        countrycolor="Black",
        showcoastlines=True,
        coastlinecolor="Black",
        showland=True,
        landcolor="white"
    ) 
    return fig

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

def generate_bars_modelweeklies(df, year, colors, model):
    start_date = str(year) + '-01-01'
    end_date = str(year) + '-12-31'   
    dfc = df[(df.Date >= start_date) & (df.Date <= end_date)]

    dfi = dfc.set_index('Date')
    dfM = dfi.resample('M').agg({'Sales':'sum'})
    
    figlinebar = px.line(x=dfM.index, y=dfM.Sales.cumsum(),
                    title = f'<b>Monthly Sales {year} {model}',
                    color_discrete_sequence = colors['colors']['palet']
                    )
    figlinebar.add_bar(x=dfM.index, y=dfM.Sales, yaxis = 'y2',
                       )
    figlinebar.update_layout(
                        yaxis=dict(
                            title='Sales',
                            ),
                        yaxis2=dict(
                            title='Profit',
                            overlaying='y',
                            side='right'
                            ),
                        legend=dict(
                            x=0.1,
                            y=1.1,
                            traceorder='normal',
                            font=dict(
                                size=12,
                                ),
                            ),
                        barmode = 'overlay'
                        )
    figlinebar.update_layout(
                        plot_bgcolor= colors['colors']['bg_figs'],
                        paper_bgcolor = colors['colors']['surround_figs'],
                        font_color = colors['colors']['text'],
#                        font_family = colors_config['colors']['font'],
                        margin = {'l':30, 'r':30, 't':80, 'b':0, 'pad':0},
                        title = {'font':{'size':18},
                                 'x':0.5,
                                 },
                        )
    
    return figlinebar

def generate_bars_rankmodel(df, year, colors):
    start_date = str(year) + '-01-01'
    end_date = str(year) + '-12-31'   
    dfc = df[(df.Date >= start_date) & (df.Date <= end_date)]

    # Group the data by Country and FuelSource and sum the Sales
    df_model = dfc.groupby(['Model'])['Sales'].sum().reset_index()
    df_model = df_model.sort_values(by = 'Sales', ascending=True)
    figbar = px.bar(df_model, x='Sales', y='Model',
                    title=f'<b>Cars Sold {year}</b>',
                    color_discrete_sequence = [colors['colors']['palet'][0]])
    figbar.update_layout(
                        plot_bgcolor= colors['colors']['bg_figs'],
                        paper_bgcolor = colors['colors']['surround_figs'],
                        font_color = colors['colors']['text'],
#                        font_family = colors_config['colors']['font'],
                        margin = {'l':30, 'r':30, 't':80, 'b':0, 'pad':0},
                        title = {'font':{'size':18},
                                 'x':0.5,
                                 },
                        )

    return figbar

def generate_bars_profitrank(df, year, colors):
    start_date = str(year) + '-01-01'
    end_date = str(year) + '-12-31'   
    dfc = df[(df.Date >= start_date) & (df.Date <= end_date)]

    # Group the data by Country and FuelSource and sum the Sales
    df_model = dfc.groupby(['Model'])['Profit'].sum().reset_index()
    df_model = df_model.sort_values(by = 'Profit', ascending=True)
    figbar = px.bar(df_model, x='Profit', y='Model',
                    title=f'<b>Net Profit {year}</b>',
                    color_discrete_sequence = [colors['colors']['palet'][1]])
    figbar.update_layout(
                        plot_bgcolor= colors['colors']['bg_figs'],
                        paper_bgcolor = colors['colors']['surround_figs'],
                        font_color = colors['colors']['text'],
#                        font_family = colors_config['colors']['font'],
                        margin = {'l':30, 'r':30, 't':80, 'b':0, 'pad':0},
                        title = {'font':{'size':18},
                                 'x':0.5,
                                 },
                        )

    return figbar

def generate_scatter_profitvssales(df, colors):
    df = df.set_index('Date')
    dfM = df.resample('M').agg({'Sales':'sum', 'Profit': 'sum', 'ProfitMargin':'mean'})
    scatter = px.scatter(dfM, x='ProfitMargin', y='Profit', color='Sales',
                         title='<b>Correlation Profit and Profit Margin</b>',
                    color_discrete_sequence = colors['colors']['palet']
                          )
    scatter.update_layout(
                        plot_bgcolor= colors['colors']['bg_figs'],
                        paper_bgcolor = colors['colors']['surround_figs'],
                        font_color = colors['colors']['text'],
#                        font_family = colors_config['colors']['font'],
                        margin = {'l':30, 'r':30, 't':80, 'b':0, 'pad':0},
                        title = {'font':{'size':18},
                                  'x':0.5,
                                  },
                        )  

    return scatter
        
def generate_dualline(df, year, colors, model):
    start_date = str(year) + '-01-01'
    end_date = str(year) + '-12-31'   
    dfc = df[(df.Date >= start_date) & (df.Date <= end_date)]
    dfm = dfc[dfc.Model == model]
    dfm = dfm.set_index('Date')
#    dfm['Profit']
    dfM = dfm.resample('M').agg({'Sales':'sum', 'Profit': 'sum', 'ProfitMargin':'mean'})

    # Create the figure
    fig = go.Figure()
    
    # Add Sales line to the figure
    fig.add_trace(go.Scatter(
        x=dfM.index, 
        y=dfM['Sales'], 
        name='Sales', 
        line=dict(color='blue'),
        yaxis='y1'
    ))
    
    # Add Profit line to the figure
    fig.add_trace(go.Scatter(
        x=dfM.index, 
        y=dfM['ProfitMargin'], 
        name='ProfitMargin', 
        line=dict(color='red'),
        yaxis='y2'
    ))
    
    # Update the layout to include two y-axes
    fig.update_layout(
        title='Sales and Profit Over Time',
        xaxis=dict(title='Date'),
        yaxis=dict(
            title='Sales',
            titlefont=dict(color='blue'),
            tickfont=dict(color='blue')
        ),
        yaxis2=dict(
            title='ProfitMargin',
            titlefont=dict(color='red'),
            tickfont=dict(color='red'),
            overlaying='y',
            side='right'
        ),
        legend=dict(x=0.1, y=1.1),
        template='plotly_white'
    )
    fig.update_layout(
                        plot_bgcolor= colors['colors']['bg_figs'],
                        paper_bgcolor = colors['colors']['surround_figs'],
                        font_color = colors['colors']['text'],
#                        font_family = colors_config['colors']['font'],
                        margin = {'l':30, 'r':30, 't':80, 'b':0, 'pad':0},
                        title = {'font':{'size':18},
                                 'x':0.5,
                                 },
                        )
    return fig

def generate_dualbar_line(df, year, colors, model):
    start_date = str(year) + '-01-01'
    end_date = str(year) + '-12-31'   
    dfc = df[(df.Date >= start_date) & (df.Date <= end_date)]
    dfm = dfc[dfc.Model == model]
    dfm = dfm.set_index('Date')
#    dfm['Profit']
    dfM = dfm.resample('M').agg({'Sales':'sum', 'Profit': 'sum', 'ProfitMargin':'mean'})

    # Create the figure
    fig = go.Figure()
    
    fig.add_trace(
        go.Bar(
            x=dfM.index,
            y = dfM.Sales,
            name='Cars Sold',
            yaxis = 'y',
            marker = dict(color=colors['colors']['palet'][0]),
            offsetgroup = 1
            )
        )
    fig.add_trace(
        go.Bar(
            x=dfM.index,
            y=dfM.Profit,
            name='Net Profit',
            yaxis='y2',
            marker = dict(color=colors['colors']['palet'][1]),
            offsetgroup = 2
            )
        )
    fig.add_trace(
        go.Scatter(
            x=dfM.index,
            y=dfM.ProfitMargin,
            mode='lines',
            name='Profit Margin',
            yaxis='y3',
            line = dict(color=colors['colors']['text'], width=3),
            marker = dict(color=colors['colors']['text']),
            )
        )
        # Update layout for multiple y-axes
    fig.update_layout(
        title=f'<b>{model} Cars Sold and Net Profit for {year}</b>',
        barmode='group',
        yaxis=dict(
            title='Cars Sold',
            titlefont=dict(color=colors['colors']['text']),
            tickfont=dict(color=colors['colors']['text']),
            showgrid=False,
        ),
        yaxis2=dict(
            title='Net Profit / ProfitMargin',
            titlefont=dict(color=colors['colors']['text']),
            tickfont=dict(color=colors['colors']['text']),
            anchor='x',
            overlaying='y',
            side='right',
            showgrid=False
        ),
        yaxis3=dict(
            title='',
            titlefont=dict(color=colors['colors']['text']),
            tickfont=dict(color=colors['colors']['text']),
            tickformat = '.1%',
            anchor='free',
            overlaying='y',
            side='right',
            position=0.995,
            showgrid=False,
            dtick = 0.005,
        ),
        xaxis=dict(
            title='Month',
            showgrid=False
        )
    )
    fig.update_layout(
                        plot_bgcolor= colors['colors']['bg_figs'],
                        paper_bgcolor = colors['colors']['surround_figs'],
                        font_color = colors['colors']['text'],
#                        font_family = colors_config['colors']['font'],
                        margin = {'l':30, 'r':30, 't':80, 'b':0, 'pad':0},
                        title = {'font':{'size':18},
                                 'x':0.5,
                                 },
                        legend = {'title': '', 'orientation':'h', 'y':1.1, 'xanchor':'left', 'x':0.03}
                        )    
    return fig

# Function to convert datetime to quarterly string format YYYYQ1
def datetime_to_quarter_str(date):
    quarter = (date.month - 1) // 3 + 1
    return f'Q{quarter}'

def generate_table_df(df, year, model):
    start_date = str(year) + '-01-01'
    end_date = str(year) + '-12-31'   
    dfc = df[(df.Date >= start_date) & (df.Date <= end_date)]
    dfm = dfc[dfc.Model == model]

    dfm = dfm.set_index('Date')
    dfQ = dfm.resample('Q').agg({'Sales':'sum', 'SalesEUR':'sum', 'Profit': 'sum', 'ProfitMargin':'mean'})
    dfQ['Cost'] = (1-dfQ.ProfitMargin) * dfQ.SalesEUR
    
    QoQ = calculate_qoq_cars_sold(df, year)

  #  dfQ['QoQ'] = QoQ['QoQ_Change']
    print(dfQ)
    
    dfQ['Sales'] = dfQ['Sales'].apply(format_large_numbers)
    dfQ['SalesEUR'] = dfQ['SalesEUR'].apply(format_large_numbers)
    dfQ['ProfitMargin'] = dfQ['ProfitMargin'].map(lambda x: f"{x:.2%}")
    dfQ['Cost'] = dfQ['Cost'].apply(format_large_numbers)
    dfQ['Profit'] = dfQ['Profit'].apply(format_large_numbers)
        
    dfQ.reset_index(inplace=True)
    dfQ['quarter'] = dfQ['Date'].apply(datetime_to_quarter_str)
    dfQ = dfQ[['Sales', 'SalesEUR', 'ProfitMargin', 'Cost', 'Profit', 'quarter']]
    dfQ['quarter'] = dfQ['quarter'].astype(str)
    dfQ = dfQ.set_index('quarter')
    
    dfQ.insert(1, 'QoQ', QoQ['QoQ_Change'])
#    dfQ['QoQ'] = dfQ['QoQ'].map(lambda x: f'{x:.2%}')
    dfQ['QoQ'] = dfQ['QoQ'].apply(format_change)

    print(dfQ)
    
    dfp = dfQ.T
    dfp.reset_index(inplace=True)
    dfp = dfp.rename(columns={'index':'Quarter'})
    
    dfp.Quarter.iloc[0] = 'Cars Sold'
    dfp.Quarter.iloc[1] = 'QoQ'
    dfp.Quarter.iloc[2] = 'Sales (€)'
    dfp.Quarter.iloc[3] = 'Profit Margin'
    dfp.Quarter.iloc[4] = 'Cost (€)'
    dfp.Quarter.iloc[5] = 'Net Profit (€)'
    
    return dfp
