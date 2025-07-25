#!/usr/bin/env python3

# Import packages
import dash
from dash import dcc, html, Input, Output, callback, State
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/page-6')

layout = html.Div([
    html.Img(src='/assets/TickTOOL_logo.png', style={'width': '40%', 'height': '40%'}, className='image-gallery'),
    html.Hr(className='orange_line'),
    html.Br(),
    html.Div([
        html.B('Confidence', style={'font-size': '60px'})
        ], style={'text-align': 'center'}),
    ######
    ######
    html.Br(),
    html.Br(),
    html.P("Please indicate your level of agreement with the following four statements :", \
           style={'font-size': '25px'}),
    html.Br(),
    html.Br(),
    html.Div([
        html.B('I am confident that I can prevent a tick bite.'),
        html.Br(),
        html.Br(),
        dcc.Dropdown(
            options=[
                {'label': 'Strongly agree', 'value': 'Strongly agree'},
                {'label': "Somewhat agree", 'value': "Somewhat agree"},
                {'label': "Neither agree nor disagree", 'value': "Neither agree nor disagree"},
                {'label': "Somewhat disagree", 'value': "Somewhat disagree"},
                {'label': "Strongly disagree", 'value': "Strongly disagree"}
            ],
            style={'width': '300px'},
            #value='',
            id = 'confidence_prevent_tick_bite'
        )
    ], style={'font-size': '20px',  'marginLeft' : '30px'}),
    html.Br(),
    html.Hr(className='grey_blue_line'),
    ######
    ######
    html.Div([
        html.B("I am confident that I could find a young tick (nymph, pictured) on my clothes or skin.",className='question_style2'),
        html.Br(),
        html.Br(),
        html.Img(src='/assets/Tick1.jpg', style={'width': '30vw', 'height': 'auto'}),
        html.Br(),
        html.Br(),
        dcc.Dropdown(
            options=[
                {'label': 'Strongly agree', 'value': 'Strongly agree'},
                {'label': "Somewhat agree", 'value': "Somewhat agree"},
                {'label': "Neither agree nor disagree", 'value': "Neither agree nor disagree"},
                {'label': "Somewhat disagree", 'value': "Somewhat disagree"},
                {'label': "Strongly disagree", 'value': "Strongly disagree"}
            ],
            style={'width': '300px'},
            #value='',
            id = 'confidence_young_tick'
        )
    ], style={'font-size': '20px',  'marginLeft' : '30px'}),
    html.Br(),
    html.Hr(className='grey_blue_line'),
    ######
    ###### 
    html.Div([
        html.B("I am confident that I could find an adult tick (pictured) on my clothes or skin."),
        html.Br(),
        html.Br(),
        html.Img(src='/assets/tick2.jpg', style={'width': '30vw', 'height': 'auto'}),
        html.Br(),
        html.Br(),
        dcc.Dropdown(
            options=[
                {'label': 'Strongly agree', 'value': 'Strongly agree'},
                {'label': "Somewhat agree", 'value': "Somewhat agree"},
                {'label': "Neither agree nor disagree", 'value': "Neither agree nor disagree"},
                {'label': "Somewhat disagree", 'value': "Somewhat disagree"},
                {'label': "Strongly disagree", 'value': "Strongly disagree"}
            ],
            style={'width': '300px'},
            #value='',
            id = 'confidence_adult_tick'
        )
    ], style={'font-size': '20px',  'marginLeft' : '30px'}),
    html.Br(),
    html.Hr(className='grey_blue_line'),
    ######
    ######
    html.Div([
        html.B("I could safely and effectively remove a tick which had embedded into the skin."
               , className= 'question_style2'),
        html.Br(),
        html.Br(),
        dcc.Dropdown(
            options=[
                {'label': 'Strongly agree', 'value': 'Strongly agree'},
                {'label': "Somewhat agree", 'value': "Somewhat agree"},
                {'label': "Neither agree nor disagree", 'value': "Neither agree nor disagree"},
                {'label': "Somewhat disagree", 'value': "Somewhat disagree"},
                {'label': "Strongly disagree", 'value': "Strongly disagree"}
            ],
            style={'width': '300px'},
            #value='',
            id = 'safely_remove_a_tick'
        )
    ], style={'font-size': '20px',  'marginLeft' : '30px'}),
    html.Br(),
    html.Br(),
    html.Div(
    [
        dcc.Link('Previous', href='/page-5', className='modern-link', style={'width': '150px', 'textAlign': 'center'}),
        dcc.Link('Next', href='/page-7', className='modern-link', style={'width': '150px', 'textAlign': 'center'}),
    ],
    style={
        'display': 'flex',
        'justifyContent': 'center',
        'alignItems': 'center',
        'gap': '40px'
        }
    ),
    html.Br(),
    html.Br(),
    dbc.Progress(value=90, style={"height": "15px"}, className="mb-3", label = "90% done"),
])
    
    

@callback(
    Output('record_answers', 'data',  allow_duplicate=True),
    Input('confidence_prevent_tick_bite', 'value'),
    Input('confidence_young_tick', 'value'),
    Input('confidence_adult_tick', 'value'),
    Input('safely_remove_a_tick', 'value'),
    State('record_answers', 'data'),
    prevent_initial_call=True,
)

def update_dic_p6(Q1,Q2,Q3,Q4,data):
    data = data or {}
    if Q1 is not None :
        data['confidence_prevent_tick_bite'] = Q1
    if Q2 is not None :
        data['confidence_young_tick'] = Q2
    if Q3 is not None :
        data['confidence_adult_tick'] = Q3
    if Q4 is not None :
        data['safely_remove_a_tick'] = Q4
    return data

@callback(
    Output('confidence_prevent_tick_bite', 'value'),
    Output('confidence_young_tick', 'value'),
    Output('confidence_adult_tick', 'value'),
    Output('safely_remove_a_tick', 'value'),
    Input('record_answers', 'data')
)
def set_dropdown_value(data):
    return (
        data.get('confidence_prevent_tick_bite', None),
        data.get('confidence_young_tick', None),
        data.get('confidence_adult_tick', None),
        data.get('safely_remove_a_tick', None)
    )


# @callback(
#     [Output('confidence_prevent_tick_bite', 'value'),
#      Output('confidence_young_tick', 'value'),
#      Output('confidence_adult_tick', 'value'),
#      Output('safely_remove_a_tick', 'value')
#     ],
#     Input('url', 'pathname'),
#     State('record_answers', 'data')
# )
  
# def initialize_inputs_page6(pathname, data):
#     if not data:
#         return [None, None]
#     return [
#      data.get('confidence_prevent_tick_bite', None),
#      data.get('confidence_young_tick', None),
#      data.get('confidence_adult_tick', None),
#      data.get('safely_remove_a_tick', None)
#      ]

# Dynamic link depending on the 'consent' answer (we skip the sociodemographic questions)
         

