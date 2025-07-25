#!/usr/bin/env python3

import dash
from dash import dcc, html, Input, Output, callback
import dash_daq as daq
import datetime
from flask import request
import re
import pandas as pd

dash.register_page(__name__, path='/methodology')

layout = html.Div([
    html.Img(src='/assets/TickTOOL_logo.png', style={'width': '40%', 'height': '40%'}, className='image-gallery'),
    html.Hr(className='orange_line'),
    html.Br(),
    html.P('Methodology', style={'font-size' : '80px', "font-weight": "bold", 'text-align': 'center'}),
    html.Br(),
    html.Br(),
    #####
   
    html.P('Potential for blacklegged tick in environment', style={'font-size' : '35px', "font-weight": "bold", 'text-align': 'center'}),
    dcc.Markdown("""Using the 6-digit postal code, an initial risk level is determined at a 1km2 resolution using habitat suitability data for Ixodes scapularis (the eastern blacklegged tick), which is then modified by the presence or absence of specific property features, as demonstrated below. Please note that these risk levels indicate risk for encountering *Ixodes scapularis*. They do not indicate risk for Lyme disease or other diseases which can be transmitted by ticks.\n\n\nRisk for *Ixodes scapularis* was computed by integrating data on temperature (cumulative annual surface degree-days above 0◦C) and suitable habitat cover (presence or absence) collected between 2018 and 2023 to give a quantitative index of risk. Further information on the methodology used to compute risk for *Ixodes scapularis* can be found at Kotchi et al (2021) [Scientific publication] (https://doi.org/10.3390/rs13030524). Using the Jenks optimisation method and Jenks natural breaks, the risk index was categorised at a 1km2 resolution into three levels: low, medium, and high. These risk levels were produced for all postal codes within Manitoba, central Canada, and eastern Canada to assess the risk of *Ixodes scapularis* (the eastern blacklegged tick). They are not applicable for assessing the risk of Ixodes pacificus (the western blacklegged tick). Individuals residing west of Manitoba are advised to consult provincial resources and eTick to learn more about potential risk for blacklegged ticks in these regions.""",  style={'marginTop': '50px', 'whiteSpace': 'pre-wrap', 'text-align': 'justify', 'marginLeft': '50px', 'marginRight': '50px'}),
    html.Img(src='/assets/BLT_in_environment_V2.png', style={'width': '40%', 'height': '40%'}, className='image-gallery'),
    
    #####
    
    html.Hr(className='orange_line'),
    html.Br(),
    html.P('Risk of exposure', style={'font-size' : '35px', "font-weight": "bold", 'text-align': 'center'}),
    dcc.Markdown("""Risk associated with outdoor activities is formulated based on prior tick exposure and the number of hours per day spent outdoors for recreational activities or in wooded areas for employment, as demonstrated below""",  style={'marginTop': '50px', 'whiteSpace': 'pre-wrap', 'text-align': 'justify', 'marginLeft': '50px', 'marginRight': '50px'}),
    html.Img(src='/assets/Risk_of_exposure_V2.png', style={'width': '15%', 'height': '15%'}, className='image-gallery'),
    
    ####
    
    html.Hr(className='orange_line'),
    html.Br(),
    html.P('Preventive behaviours', style={'font-size' : '35px', "font-weight": "bold", 'text-align': 'center'}),
    dcc.Markdown("""Risk associated with the level of adoption of preventive behaviours is formulated based on user responses related to various preventive behaviours and whether the user knows or suspects they have visited or lived in a region where they could contact a disease transmitted by ticks (see below). This risk level does consider actual environmental risk (based on postal code) as this is provided separately. The objective of this risk level is to encourage users to reflect on which preventive behaviours they are currently implementing and would like to implement in the future based on their environmental risk and risk due to outdoor activities. """,  style={'marginTop': '50px', 'whiteSpace': 'pre-wrap', 'text-align': 'justify', 'marginLeft': '50px', 'marginRight': '50px'}),

    html.Img(src='/assets/Preventive_behaviours_V2.png', style={'width': '40%', 'height': '40%'}, className='image-gallery'),
    ####
    
    html.Br(),
    html.Br(),
    
    ])
