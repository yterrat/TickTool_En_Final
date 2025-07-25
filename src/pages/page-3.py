#!/usr/bin/env python3

# Import packages
import dash
from dash import dcc, html, Input, Output, callback, State
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/page-3')

layout = html.Div([
    html.Img(src='/assets/TickTOOL_logo.png', style={'width': '40%', 'height': '40%'}, className='image-gallery'),
    html.Hr(className='orange_line'),
    html.Br(),
    html.Div([
        html.B('Outdoor activities', style={'font-size': '60px'})
        ], style={'text-align': 'center'}),
    html.Br(),
    html.Br(),
    html.B("As part of your primary occupation (including work or studies), \
           on average how much time do you spend daily in wooded or grassy areas between the months of April and November? ", style={'font-size': '20px'}),
    html.Br(),
    html.Br(),
    html.Div([
            dcc.Dropdown(
                options=[
                    {'label': 'Never', 'value': 'Never'},
                    {'label': 'Less than one hour per day', 'value': 'Less than one hour per day'},
                    {'label': 'Between one and five hours per day', 'value': 'Between one and five hours per day'},
                    {'label': 'More than five hours per day', 'value': 'More than five hours per day'},
                    {'label': 'Not applicable to my situation', 'value': 'Not applicable to my situation'}
                ],
                style={'width': '400px'},
                #value='',
                id = 'time_daily_wooded_area'
            ),
        ], style={'font-size': '15px', 'marginLeft' : '30px'}),
    html.Br(),
    #######
    #######
    html.Hr(className='grey_blue_line'),
    html.Br(),
    html.B('How often do you engage in the following outdoor activities between the months of April and November \
           (Examples include walking or hiking, camping, hunting, gardening/yard work, \
            recreational sports, woodcutting, foraging)?',  style={'font-size': '20px'}),
    html.Br(),
    html.Br(),
    html.Div([
        dcc.Dropdown(
            options=[
                {'label': 'Never', 'value': 'Never'},
                {'label': 'Rarely (Fewer than 2 times a year)', 'value': 'Rarely (Fewer than 2 times a year)'},
                {'label': 'Often (From 2 to 10 times a year)', 'value': 'Often (From 2 to 10 times a year)'},
                {'label': 'Very often (More than 10 times a year)', 'value': 'Very often (More than 10 times a year)'}
            ],
            style={'width': '400px'},
            #value='',
            id = 'frequency_outdoor_activities'
        )
    ], style={'font-size': '15px', 'marginLeft' : '30px'}),
    html.Br(),
    html.Br(), 
    html.Div(
    [
        dcc.Link('Previous', href='/page-2', className='modern-link', style={'width': '150px', 'textAlign': 'center'}),
        dcc.Link('Next', href='/page-4', className='modern-link', style={'width': '150px', 'textAlign': 'center'}),
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
    dbc.Progress(value=33, style={"height": "15px"}, className="mb-3", label = "33% done"),
    html.Br(),
    #html.Div(id='display-answers3', style={'marginTop': '50px', 'whiteSpace': 'pre-wrap'})
])
           

@callback(
      Output('record_answers', 'data',  allow_duplicate=True),
      Input('time_daily_wooded_area', 'value'),
      Input('frequency_outdoor_activities', 'value'),
      State('record_answers', 'data'),
      prevent_initial_call=True,
)

def update_dic_page3(Q1,Q2,data):
      data = data or {}
      if Q1 is not None :
          data['time_daily_wooded_area'] = Q1
      if Q2 is not None :
        data['frequency_outdoor_activities'] = Q2
      return data
  
@callback(
    Output('time_daily_wooded_area', 'value'),
    Output('frequency_outdoor_activities', 'value'),
    Input('record_answers', 'data')
)
def set_dropdown_value(data):
    return (
        data.get('time_daily_wooded_area', None),
        data.get('frequency_outdoor_activities', None)
    )

 
# @callback(
#     Output('display-answers3', 'children'),
#     Input('record_answers', 'data')
# )

# def display_answers_p3(data):
#     if data:
#         return html.Pre(json.dumps(data, indent=2))
#     return "No data recorded yet."
