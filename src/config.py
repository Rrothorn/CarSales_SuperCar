# -*- coding: utf-8 -*-
"""
Created on Sun May  5 23:16:38 2024

@author: Gebruiker
"""
import plotly.express as px

colors_config= {
    'colors' : {
        'bg_figs': '#FFFFFF',
        "surround_figs": '#5B706F',
        'text': '#7FDBFF',
        'font': 'Lato',
#        'palet': ['#294867', '#98691E', '#672967', '#1C778A', '#C0C0C0']
#        'palet': ['#50ED12', '#ED6812', '#EDC212', '#176B84', '#C0C0C0']
        'palet': ['#0f3e62', '#63a2bb', '#3d6581', '#86ccdc', '#1a9991', '#3fada7', '#7cdf91', '#b9e99a']
        }    
    }

# card style
card_config = {
    'cardstyle' : {
        'border-radius': '15px',
        'border':'1px solid #C5C5C5',
        'background-color':colors_config['colors']['surround_figs'],
        },
    'cardtitle' : {
        'color': colors_config['colors']['text'],
        'font-size':'17px',
        'font-weight':'bold'
        },
    'cardtext' : {
        'color': '#FFFFFF',
        'font-size':'17px',
        'font-weight':'bold'
        },
    } 

color_schemes = dict(
    White_MonoBlue = dict(
                          colors_config = {
                                'colors' : {
                                    'background': '#FAF9F2',
                                    'background-image': 'linear-gradient(to left, rgba(250,249,242,1), rgba(250,249,242,1))',
                                    'bg_figs': '#FFFFFF',
                                    'surround_figs': '#FFFFFF',
                                    'text': '#000000',
                                    'font': 'Lato',
                                    'palet': ['#0f3e62', '#63a2bb', '#3d6581', '#86ccdc', '#1a9991', '#3fada7', '#7cdf91', '#b9e99a'],
                                    'heatmap': px.colors.sequential.Blues, 
                                    },                              
                                },   
                          ),
    White_MonoYellow = dict(
                          colors_config = {
                                'colors' : {
                                    'background': '#FAF9F2',
                                    'background-image': 'linear-gradient(to left, rgba(250,249,242,1), rgba(250,249,242,1))',
                                    'bg_figs': '#FFFFFF',
                                    'surround_figs': '#FFFFFF',
                                    'text': '#000000',
                                    'font': 'Verdana',
                                    'palet': ['#b51b43','#f5b849', '#e38d34', '#f79845', '#f8d293', '#e7311b', '#e3513e', '#f8c294'],
                                    'heatmap': px.colors.sequential.YlOrRd, 
                                    },                              
                                },   
                          ),
    Black_Rain = dict(
                          colors_config = {
                                'colors' : {
                                    'background': '#000000',
                                    'background-image': 'linear-gradient(to left, rgba(0,0,0,1), rgba(0,0,0,1))',
                                    'bg_figs': '#000000',
                                    'surround_figs': '#000000',
                                    'text': '#FFFFFF',
                                    'font': 'Verdana',
                                    'palet': ['#12B18A','#7312B1', '#B11265', '#B14E12', '#f8d293', '#e7311b', '#e3513e', '#f8c294'],
                                    'heatmap': px.colors.sequential.Plasma, 
                                    },                              
                                },   
                          ),

    Greys_Bright = dict(
                          colors_config = {
                                'colors' : {
                                    'background': '#4D4D4D',
                                    'background-image': 'linear-gradient(to left, rgba(77,77,77,0.5), rgba(77,77,77,1))',
                                    'bg_figs': '#616161',
                                    'surround_figs': '#454545',
                                    'text': '#FFFFFF',
                                    'font': 'verdana',
                                    'palet': ['#007677','#BF1295', '#BFB300', '#7E12BF', '#f8d293', '#e7311b', '#e3513e', '#f8c294'],
                                    'heatmap': px.colors.sequential.Viridis, 
                                    },                              
                                },   
                          ),    
    
    DarkBlue_Orange = dict(
                          colors_config = {
                                'colors' : {
                                    'background': '#000000',
                                    'background-image': 'linear-gradient(to left, rgba(28,51,78,0.5), rgba(28,51,78,1))',
                                    'bg_figs': '#2B4E76',
                                    'surround_figs': '#0F1F37',
                                    'text': '#FFFFFF',
                                    'font': 'Verdana',
                                    'palet': ['#FA4201', '#C23300','#DA3900', '#5E1A02', '#f8d293', '#e7311b', '#e3513e', '#f8c294'],
                                    'heatmap': px.colors.sequential.Oranges, 
                                    },                              
                                },   
                          ),
    DarkBlue_Trq = dict(
                          colors_config = {
                                'colors' : {
                                    'background': '#000000',
                                    'background-image': 'linear-gradient(to left, rgba(28,51,78,0.5), rgba(28,51,78,1))',
                                    'bg_figs': '#2B4E76',
                                    'surround_figs': '#0F1F37',
                                    'text': '#FFFFFF',
                                    'font': 'Verdana',
                                    'palet': ['#016150','#02957A', '#01FACB', '#01D1AA', '#f8d293', '#e7311b', '#e3513e', '#f8c294'],
                                    'heatmap': px.colors.sequential.Bluyl, 
                                    },                              
                                },   
                          ),
                    )

card_configs = dict(
    White_MonoBlue = dict(card_config = {
                            'cardstyle': {
                                'border-radius': '10px',
                                'border':'1px solid #C5C5C5',
                                'background-color':'#FFFFFF',
                                'background-image': 'linear-gradient(to left, rgba(255,255,255,1), rgba(255,255,255,1))',
                                'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                },
                            'cardtitle': {
                                'color': color_schemes['White_MonoBlue']['colors_config']['colors']['text'],
                                'font-size':'22px',
                                'font-weight':'bold',
                                'align':'center'
                                },
                            'cardvalue': {
                                'color': color_schemes['White_MonoBlue']['colors_config']['colors']['palet'][0],
                                'font-size':'20px',
                                'font-weight':'bold'
                                }
                            },    
                         ),
    White_MonoYellow = dict(card_config = {
                            'cardstyle': {
                                'border-radius': '10px',
                                'border':'1px solid #C5C5C5',
                                'background-color':'#FFFFFF',
                                'background-image': 'linear-gradient(to left, rgba(255,255,255,1), rgba(255,255,255,1))',
                                'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                },
                            'cardtitle': {
                                'color': color_schemes['White_MonoYellow']['colors_config']['colors']['text'],
                                'font-size':'22px',
                                'font-weight':'bold',
                                'align':'center'
                                },
                            'cardvalue': {
                                'color': color_schemes['White_MonoYellow']['colors_config']['colors']['palet'][0],
                                'font-size':'20px',
                                'font-weight':'bold'
                                }
                            },    
                         ),
    Black_Rain = dict(card_config = {
                            'cardstyle': {
                                'border-radius': '10px',
                                'border':'1px solid #494949',
                                'background-color':'#000000',
                                'background-image': 'linear-gradient(to left, rgba(0,0,0,1), rgba(0,0,0,1))',
                                'boxShadow': '0 4px 8px 0 rgba(255, 255, 255, 0.1), 0 6px 20px 0 rgba(255, 255, 255, 0.15)',
                                },
                            'cardtitle': {
                                'color': color_schemes['Black_Rain']['colors_config']['colors']['text'],
                                'font-size':'22px',
                                'font-weight':'bold',
                                'align':'center'
                                },
                            'cardvalue': {
                                'color': color_schemes['Black_Rain']['colors_config']['colors']['palet'][0],
                                'font-size':'20px',
                                'font-weight':'bold'
                                }
                            },    
                         ),
    
    Greys_Bright = dict(card_config = {
                            'cardstyle': {
                                'border-radius': '10px',
                                'border':'1px solid #494949',
                                'background-color':'#303030',
                                'background-image': 'linear-gradient(to left, rgba(48,48,48,1), rgba(48,48,48,0.5))',
                                'boxShadow': '0 4px 8px 0 rgba(255, 255, 255, 0.1), 0 6px 20px 0 rgba(255, 255, 255, 0.15)',
                                },
                            'cardtitle': {
                                'color': color_schemes['Greys_Bright']['colors_config']['colors']['text'],
                                'font-size':'22px',
                                'font-weight':'bold',
                                'align':'center'
                                },
                            'cardvalue': {
                                'color': color_schemes['Greys_Bright']['colors_config']['colors']['palet'][0],
                                'font-size':'20px',
                                'font-weight':'bold'
                                }
                            },    
                         ),
    
    DarkBlue_Orange = dict(card_config = {
                            'cardstyle': {
                                'border-radius': '10px',
                                'border':'1px solid #494949',
                                'background-color':'#000000',
                                'background-image': 'linear-gradient(to left, rgba(28,51,78,0.5), rgba(28,51,78,1))',
                                'boxShadow': '0 4px 8px 0 rgba(255, 255, 255, 0.1), 0 6px 20px 0 rgba(255, 255, 255, 0.15)',
                                },
                            'cardtitle': {
                                'color': color_schemes['DarkBlue_Orange']['colors_config']['colors']['text'],
                                'font-size':'22px',
                                'font-weight':'bold',
                                'align':'center'
                                },
                            'cardvalue': {
                                'color': color_schemes['DarkBlue_Orange']['colors_config']['colors']['palet'][0],
                                'font-size':'20px',
                                'font-weight':'bold'
                                }
                            },    
                         ),
    DarkBlue_Trq = dict(card_config = {
                            'cardstyle': {
                                'border-radius': '10px',
                                'border':'1px solid #494949',
                                'background-color':'#000000',
                                'background-image': 'linear-gradient(to left, rgba(28,51,78,0.5), rgba(28,51,78,1))',
                                'boxShadow': '0 4px 8px 0 rgba(255, 255, 255, 0.1), 0 6px 20px 0 rgba(255, 255, 255, 0.15)',
                                },
                            'cardtitle': {
                                'color': color_schemes['DarkBlue_Trq']['colors_config']['colors']['text'],
                                'font-size':'22px',
                                'font-weight':'bold',
                                'align':'center'
                                },
                            'cardvalue': {
                                'color': color_schemes['DarkBlue_Trq']['colors_config']['colors']['palet'][0],
                                'font-size':'20px',
                                'font-weight':'bold'
                                }
                            },    
                         ),      
                )       

