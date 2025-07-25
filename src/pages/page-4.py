#!/usr/bin/env python3

# Import packages
import dash
from dash import dcc, html, Input, Output, callback, State
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/page-4')

layout = html.Div([
    html.Img(src='/assets/TickTOOL_logo.png', style={'width': '40%', 'height': '40%'}, className='image-gallery'),
    html.Hr(className='orange_line'),
    html.Br(),
    html.Div([
        html.B('Self-protection', style={'font-size': '60px'})
        ], style={'text-align': 'center'}),
    html.Br(),
    html.Br(),
    html.B("In the last year, have you visited an area where you knew or suspected you could \
           contract Lyme disease, or another disease spread by ticks?", style={'font-size': '20px'}),
    html.Br(),
    html.Br(),
    html.Div([
            dcc.Dropdown(
                options=[
                    {'label': 'Yes', 'value': 'yes'},
                    {'label': 'No', 'value': 'no'},
                    {'label': "I don't know", 'value': "I don't know"}
                ],
                style={'width': '200px'},
                #value='',
                id = 'visite_area_disease_ticks'
            ),
        ], style={'font-size': '15px', 'marginLeft' : '30px'}),
    html.Br(),
    html.Hr(className='grey_blue_line'),
    html.B("In the last year, have you searched for information on ways of protecting yourself from diseases transmitted by ticks?", style={'font-size': '20px'}),
    html.Br(),
    html.Br(),
    html.Div([
            dcc.Dropdown(
                options=[
                    {'label': 'Yes', 'value': 'yes'},
                    {'label': 'No', 'value': 'no'},
                    {'label': "I don't know", 'value': "I don't know"}
                ],
                style={'width': '200px'},
                #value='',
                id = 'search_for_informations_ticks'
            ),
        ], style={'font-size': '15px', 'marginLeft' : '30px'}),
    html.Br(),
    #######
    #######
    html.Div(
        id='visite_area_disease_ticks_questions',
        children=[
            html.Br(),
            html.Div(
                id='visiting_Lyme_area',
                children=[
                    html.Hr(className='grey_blue_line'),
                    html.Br(),
                    html.B("When in known risk areas, how frequently did you adopt the following measures \
                           to protect yourself, while or after being in a wooded area? ", style={'font-size': '20px'}),
                    html.Br(),
                    html.Br(),
                    html.B("When spending time in risk areas:", style={'font-size': '20px'}),
                    html.Br(),
                    html.Br(),
                    html.Div([
                        html.Div([
                            html.Label('Wearing long layers of clothing (e.g., pants, long sleeves).',  style={'font-size': '20px'}),
                            html.Br(),
                            html.Br(),
                            dcc.Dropdown(
                                options=[
                                    {'label': 'Never', 'value': 'Never'},
                                    {'label': 'Rarely', 'value': 'Rarely'},
                                    {'label': 'Sometimes', 'value': 'Sometimes'},
                                    {'label': "Most of the time", 'value': "Most of the time"},
                                    {'label': "Always", 'value': "Always"},
                                    {'label': "Not applicable", 'value': "Not applicable"}
                                ],
                                style={'width': '200px'},
                                #value='',
                                id = 'Wearing_long_layers_of_clothing'
                            )
                        ], style={'font-size': '15px', 'marginLeft' : '30px'}),
                        html.Br(),
                        html.Div([
                            html.Label('Wearing light-coloured clothing.',  style={'font-size': '20px'}),
                            html.Br(),
                            html.Br(),
                            dcc.Dropdown(
                                options=[
                                    {'label': 'Never', 'value': 'Never'},
                                    {'label': 'Rarely', 'value': 'Rarely'},
                                    {'label': 'Sometimes', 'value': 'Sometimes'},
                                    {'label': "Most of the time", 'value': "Most of the time"},
                                    {'label': "Always", 'value': "Always"},
                                    {'label': "Not applicable", 'value': "Not applicable"}
                                ],
                                style={'width': '200px'},
                                #value='',
                                id = 'Wearing_light-coloured_clothing'
                            )
                        ], style={'font-size': '15px', 'marginLeft' : '30px'}),
                        html.Br(),
                        html.Div([
                            html.Label('Tucking in clothes',  style={'font-size': '20px'}),
                            html.Br(),
                            html.Br(),
                            dcc.Dropdown(
                                options=[
                                    {'label': 'Never', 'value': 'Never'},
                                    {'label': 'Rarely', 'value': 'Rarely'},
                                    {'label': 'Sometimes', 'value': 'Sometimes'},
                                    {'label': "Most of the time", 'value': "Most of the time"},
                                    {'label': "Always", 'value': "Always"},
                                    {'label': "Not applicable", 'value': "Not applicable"}
                                ],
                                style={'width': '200px'},
                                #value='',
                                id = 'Tucking_in_clothes'
                            )
                        ], style={'font-size': '15px', 'marginLeft' : '30px'}),
                        html.Br(),
                        html.Div([
                            html.Label('Applying bug repellent containing DEET or icaridin (also known as picaridin) to skin or clothing. ',  style={'font-size': '20px'}),
                            html.Br(),
                            html.Br(),
                            dcc.Dropdown(
                                options=[
                                    {'label': 'Never', 'value': 'Never'},
                                    {'label': 'Rarely', 'value': 'Rarely'},
                                    {'label': 'Sometimes', 'value': 'Sometimes'},
                                    {'label': "Most of the time", 'value': "Most of the time"},
                                    {'label': "Always", 'value': "Always"},
                                    {'label': "Not applicable", 'value': "Not applicable"}
                                ],
                                style={'width': '200px'},
                                #value='',
                                id = 'DEET'
                            )
                        ], style={'font-size': '15px', 'marginLeft' : '30px'}),
                        html.Br(),
                        html.Div([
                            html.Label('Walking on cleared paths and trails ',  style={'font-size': '20px'}),
                            html.Br(),
                            html.Br(),
                            dcc.Dropdown(
                                options=[
                                    {'label': 'Never', 'value': 'Never'},
                                    {'label': 'Rarely', 'value': 'Rarely'},
                                    {'label': 'Sometimes', 'value': 'Sometimes'},
                                    {'label': "Most of the time", 'value': "Most of the time"},
                                    {'label': "Always", 'value': "Always"},
                                    {'label': "Not applicable", 'value': "Not applicable"}
                                ],
                                style={'width': '200px'},
                                #value='',
                                id = 'Walking_on_cleared_paths'
                            )
                        ], style={'font-size': '15px', 'marginLeft' : '30px'}),
                    ]),
                    html.Br(),
                    html.B("After being in risk areas:", style={'font-size': '20px'}),
                    html.Br(),
                    html.Br(),
                    html.Div([
                        html.Div([
                            html.Label('Examining your clothes to avoid bringing ticks into your home ',  style={'font-size': '20px'}),
                            html.Br(),
                            html.Br(),
                            dcc.Dropdown(
                                options=[
                                    {'label': 'Never', 'value': 'Never'},
                                    {'label': 'Rarely', 'value': 'Rarely'},
                                    {'label': 'Sometimes', 'value': 'Sometimes'},
                                    {'label': "Most of the time", 'value': "Most of the time"},
                                    {'label': "Always", 'value': "Always"},
                                    {'label': "Not applicable", 'value': "Not applicable"}
                                ],
                                style={'width': '200px'},
                                #value='',
                                id = 'Examining_your_clothes'
                            )
                        ], style={'font-size': '15px', 'marginLeft' : '30px'}),
                        html.Br(),
                        html.Div([
                            html.Label('Putting your clothes in the dryer on high heat to kill ticks',  style={'font-size': '20px'}),
                            html.Br(),
                            html.Br(),
                            dcc.Dropdown(
                                options=[
                                    {'label': 'Never', 'value': 'Never'},
                                    {'label': 'Rarely', 'value': 'Rarely'},
                                    {'label': 'Sometimes', 'value': 'Sometimes'},
                                    {'label': "Most of the time", 'value': "Most of the time"},
                                    {'label': "Always", 'value': "Always"},
                                    {'label': "Not applicable", 'value': "Not applicable"}
                                ],
                                style={'width': '200px'},
                                #value='',
                                id = 'clothes_in_the_dryer'
                            )
                        ], style={'font-size': '15px', 'marginLeft' : '30px'}),
                        html.Br(),
                        html.Div([
                            html.Label('Examining yourself to find and remove ticks within 24h',  style={'font-size': '20px'}),
                            html.Br(),
                            html.Br(),
                            dcc.Dropdown(
                                options=[
                                    {'label': 'Never', 'value': 'Never'},
                                    {'label': 'Rarely', 'value': 'Rarely'},
                                    {'label': 'Sometimes', 'value': 'Sometimes'},
                                    {'label': "Most of the time", 'value': "Most of the time"},
                                    {'label': "Always", 'value': "Always"},
                                    {'label': "Not applicable", 'value': "Not applicable"}
                                ],
                                style={'width': '200px'},
                                #value='',
                                id = 'Examining_yourself'
                            )
                        ], style={'font-size': '15px', 'marginLeft' : '30px'}),
                        html.Br(),
                        html.Div([
                            html.Label('Bathing or showering after being in risk areas.',  style={'font-size': '20px'}),
                            html.Br(),
                            html.Br(),
                            dcc.Dropdown(
                                options=[
                                    {'label': 'Never', 'value': 'Never'},
                                    {'label': 'Rarely', 'value': 'Rarely'},
                                    {'label': 'Sometimes', 'value': 'Sometimes'},
                                    {'label': "Most of the time", 'value': "Most of the time"},
                                    {'label': "Always", 'value': "Always"},
                                    {'label': "Not applicable", 'value': "Not applicable"}
                                ],
                                style={'width': '200px'},
                                #value='',
                                id = 'Bathing_or_showering'
                            )
                        ], style={'font-size': '15px', 'marginLeft' : '30px'}),
                        html.Br(),
                    ])
                ], style={'display':'block'}
            ),
        ]),
    ######
    ######
    html.Br(),
    html.Div(
    [
        dcc.Link('Previous', href='/page-3', className='modern-link', style={'width': '150px', 'textAlign': 'center'}),
        dcc.Link('Next', href='/page-5', className='modern-link', style={'width': '150px', 'textAlign': 'center'}),
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
    dbc.Progress(value=50, style={"height": "15px"}, className="mb-3", label = "50% done"),
    html.Br(),
    html.Br(),
    #html.Div(id='display-answers4', style={'marginTop': '50px', 'whiteSpace': 'pre-wrap'})
])
                   
            

@callback(
    Output('record_answers', 'data',  allow_duplicate=True),
    Input('visite_area_disease_ticks', 'value'),
    Input('search_for_informations_ticks', 'value'),
    Input('Wearing_long_layers_of_clothing', 'value'),
    Input('Wearing_light-coloured_clothing', 'value'),
    Input('Tucking_in_clothes', 'value'),
    Input('DEET', 'value'),
    Input('Walking_on_cleared_paths', 'value'),
    Input('Examining_your_clothes', 'value'),
    Input('clothes_in_the_dryer', 'value'),
    Input('Examining_yourself', 'value'),
    Input('Bathing_or_showering', 'value'),
    State('record_answers', 'data'),
    prevent_initial_call=True,
)

def update_dic_p4(Q1,Q2,Q3,Q4,Q5,Q6,Q7,Q8,Q9,Q10,Q11,data):
    data = data or {}
    if Q1 is not None :
        data['visite_area_disease_ticks'] = Q1
    if Q2 is not None :
        data['search_for_informations_ticks'] = Q2 
    if Q3 is not None :   
        data['Wearing_long_layers_of_clothing'] = Q3
    if Q4 is not None :
        data['Wearing_light-coloured_clothing'] = Q4
    if Q5 is not None :
        data['Tucking_in_clothes'] = Q5
    if Q6 is not None :
        data['DEET'] = Q6
    if Q7 is not None :
        data['Walking_on_cleared_paths'] = Q7
    if Q8 is not None :
        data['Examining_your_clothes'] = Q8
    if Q9 is not None :
        data['clothes_in_the_dryer'] = Q9
    if Q10 is not None :
        data['Examining_yourself'] = Q10
    if Q11 is not None :
        data['Bathing_or_showering'] = Q11
    return data


@callback(
    Output('visite_area_disease_ticks', 'value'),
    Output('search_for_informations_ticks', 'value'),
    Output('Wearing_long_layers_of_clothing', 'value'),
    Output('Wearing_light-coloured_clothing', 'value'),
    Output('Tucking_in_clothes', 'value'),
    Output('DEET', 'value'),
    Output('Walking_on_cleared_paths', 'value'),
    Output('Examining_your_clothes', 'value'),
    Output('clothes_in_the_dryer', 'value'),
    Output('Examining_yourself', 'value'),
    Output('Bathing_or_showering', 'value'),
    Input('record_answers', 'data')
)
def set_dropdown_value(data):
    return (
        data.get('visite_area_disease_ticks', None),
        data.get('search_for_informations_ticks', None),
        data.get('Wearing_long_layers_of_clothing', None),
        data.get('Wearing_light-coloured_clothing', None),
        data.get('Tucking_in_clothes', None),
        data.get('DEET', None),
        data.get('Walking_on_cleared_paths', None),
        data.get('Examining_your_clothes', None),
        data.get('clothes_in_the_dryer', None),
        data.get('Examining_yourself', None),
        data.get('Bathing_or_showering', None)
    )

@callback(
    Output(component_id='visite_area_disease_ticks_questions', component_property='hidden'),
    [Input(component_id='visite_area_disease_ticks', component_property='value')])

def show_hide_element_visite_area_disease_ticks(visite_area_disease_ticks):
    if visite_area_disease_ticks == 'yes':
        return False
    else:
        return True



# @callback(
#     [Output('visite_area_disease_ticks', 'value'),
#      Output('Wearing_long_layers_of_clothing', 'value'),
#      Output('Wearing_light-coloured_clothing', 'value'),
#      Output('Tucking_in_clothes', 'value'),
#      Output('DEET', 'value'),
#      Output('Walking_on_cleared_paths', 'value'),
#      Output('Examining_your_clothes', 'value'),
#      Output('clothes_in_the_dryer', 'value'),
#      Output('Examining_yourself', 'value'),
#      Output('Bathing_or_showering', 'value')
#     ],
#     Input('url', 'pathname'),
#     State('record_answers', 'data')
# )
  
# def initialize_inputs_page4(pathname, data):
#     if not data:
#         return [None, None]
#     return [
#      data.get('visite_area_disease_ticks', None),
#      data.get('Wearing_long_layers_of_clothing', None),
#      data.get('Wearing_light-coloured_clothing', None),
#      data.get('Tucking_in_clothes', None),
#      data.get('DEET', None),
#      data.get('Walking_on_cleared_paths', None),
#      data.get('Examining_your_clothes', None),
#      data.get('clothes_in_the_dryer', None),
#      data.get('Examining_yourself', None),
#      data.get('Bathing_or_showering', None),
#      ]
         
 
# @callback(
#     Output('display-answers4', 'children'),
#     Input('record_answers', 'data')
# )

# def display_answers_p4(data):
#     if data:
#         return html.Pre(json.dumps(data, indent=2))
#     return "No data recorded yet."



