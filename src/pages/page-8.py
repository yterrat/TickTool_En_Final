#!/usr/bin/env python3

# Import packages
import dash
from dash import dcc, html, Input, Output, callback
import dash_daq as daq
import datetime
from flask import request
import re
import pandas as pd
import json
import plotly.graph_objs as go


#Zipcode section
df_zipcodes = pd.read_csv('Zipcodes_dereplicate.csv')
risk_dict = dict(zip(df_zipcodes['POSTALCODE'], df_zipcodes['RISK']))

#Keys tab
mykeys = [
  "consent",
  "zipcode",
  "which_residence",
  "previous_completion",
  "live_alone",
  "live_with_child_0_4",
  "live_with_child_5_14",
  "live_with_child_15_18",
  "live_with_someone_over_18",
  "dog",
  "cat",
  "horse",
  "anti_tick_treatment_dog",
  "vaccination_treatment_dog",
  "anti_tick_treatment_cat",
  "house_proximity_wooded_area",
  "access_courtyard",
  "house_deer",
  "courtyard_herbaceous_or_forest",
  "courtyard_children_play_area",
  "courtyard_fences_deer",
  "courtyard_corridor",
  "courtyard_mowing",
  "courtyard_fallen_leaves",
  "courtyard_clearing_herbaceous",
  "time_daily_wooded_area",
  "frequency_outdoor_activities",
  "visite_area_disease_ticks",
  "search_for_informations_ticks",
  "Wearing_long_layers_of_clothing",
  "Wearing_light-coloured_clothing",
  "Tucking_in_clothes",
  "DEET",
  "Walking_on_cleared_paths",
  "Examining_your_clothes",
  "clothes_in_the_dryer",
  "Examining_yourself",
  "Bathing_or_showering",
  "attached_to_your_skin",
  "Freely_moving",
  "On_a_pet",
  "Freely_moving_outside",
  "How_many_embedded_in_your_skin",
  "How_many_freely_moving_on_your_skin",
  "How_many_on_a_pet",
  "confidence_prevent_tick_bite",
  "confidence_young_tick",
  "confidence_adult_tick",
  "safely_remove_a_tick",
  "Age",
  "Education",
  "Employment_status",
  "Income",
  "primary_language",
  "population_group",
  "population_group_text",
  "commentaries"
]

def build_gauge_figure(value, color_ranges):
    import plotly.graph_objects as go

    active_key = None
    for clr, rng in color_ranges.items():
        if rng[0] <= value < rng[1]:
            active_key = clr
            break
    if value >= 3:
        active_key = list(color_ranges.keys())[-1]

    # Color maps
    steps = []
    color_map = {
        'grey': 'rgba(128,128,128,0.8)',
        'limegreen': 'rgba(50,205,50,0.8)',
        'orange': 'rgba(255,165,0,0.8)',
        'red': 'rgba(255,0,0,0.8)',
    }
    full_opacity_map = {
        'grey': 'rgba(128,128,128,1)',
        'limegreen': 'rgba(50,205,50,1)',
        'orange': 'rgba(255,165,0,1)',
        'red': 'rgba(255,0,0,1)',
    }

    for clr, rng in color_ranges.items():
        steps.append({
            'range': rng,
            'color': full_opacity_map[clr] if clr == active_key else color_map[clr]
        })

    # Label formatting
    labels = ['Low', 'Moderate', 'High']
    bold = lambda text: f'<b>{text}</b>'
    faded = lambda text: f'<span style="color:lightgray">{text}</span>'

    if 0.1 <= value < 1:
        ticktext = [bold('Low'), faded('Moderate'), faded('High')]
    elif 1 <= value < 2:
        ticktext = [faded('Low'), bold('Moderate'), faded('High')]
    elif 2 <= value <= 3:
        ticktext = [faded('Low'), faded('Moderate'), bold('High')]
    else:
        ticktext = labels

    # Gauge creation
    fig = go.Figure(go.Indicator(
        mode="gauge",
        value=value,
        gauge={
            'axis': {
                'range': [0, 3],
                'tickvals': [0.6, 1.5, 2.4],
                'ticktext': ticktext,
                'tickangle': 0,
                'tickfont': {'size': 18},
            },
            'bar': {'color': 'black', 'thickness': 0.2},
            'steps': steps,
        },
        domain={'x': [0, 1], 'y': [0, 1]},
        number={'valueformat': '.2f', 'font': {'color': 'rgba(0,0,0,0)'}}
    ))

    layout_config = {
        "margin": dict(t=10, b=130, l=40, r=40),  # extra space for bottom text
        "paper_bgcolor": "white",
    }

    # If invalid data, add visible warning
    if value == 0.05:
        layout_config["margin"] = dict(t=10, b=180, l=40, r=40)
        layout_config["annotations"] = [
            dict(
                text=(
                    "<b>⚠️ Score not computed</b><br>"
                    "Some answers were missing or incomplete.<br>"
                    "Please complete the questionnaire and try again."
                ),
                x=0.5,
                y=-0.15,  # was -0.35
                xref='paper',
                yref='paper',
                showarrow=False,
                font=dict(size=20, color="black"),
                align='center',
                xanchor='center',
                yanchor='top',
                borderpad=10,
                bgcolor='rgba(255,255,255,0.9)',
            )
        ]

    fig.update_layout(**layout_config)
    return fig



# Function to build the full Dash component
def build_gauge(gauge_id, value, color_ranges):
    fig = build_gauge_figure(value, color_ranges)
    return dcc.Graph(id=gauge_id, figure=fig, style={'height': '500px', 'width': '500px'})


#######


dash.register_page(__name__, path='/page-8')

layout = html.Div([
    html.Div(id='score_summary', style={'text-align': 'center', 'font-size': '24px', 'margin-top': '30px'}),
    html.Img(src='/assets/TickTOOL_logo.png', style={'width': '40%', 'height': '40%'}, className='image-gallery'),
    html.Hr(className='orange_line'),
    html.Br(),
    html.Div([
        html.B('Your personalized report', style={'font-size': '60px'})
    ], style={'text-align': 'center'}),
    html.Br(),
    html.P("Here is a legend that will help you understand the meaning of the colors :", style={'fontSize': '20px','textAlign': 'center','marginTop': '20px','marginBottom': '20px'  }),
    html.Br(),
    html.Img(src='/assets/legend_p8.png', style={'width': '60%', 'height': '60%'}, className='image-gallery'),
    html.Br(),
    html.P('"The greener the score, the lower your risk of being bitten by a tick and the better your prevention strategies."', style={'fontSize': '32px','textAlign': 'center','marginTop': '20px','marginBottom': '20px', 'font-weight': 'bold' }),
    html.Br(),
    html.Hr(className='orange_line'),
    #############
    # SECTION 1 #
    #############
    html.Br(),
    html.Div([
        html.P(
            'Potential presence of blacklegged ticks in your environment',
            style={
                'fontSize': '40px',
                'textAlign': 'center',
                'marginTop': '20px',
                'marginBottom': '20px',
                'fontWeight': 'bold'  # optional: makes it more prominent
            }
        ),
        html.Div([
            build_gauge('gauge1', 0.05, {'grey': [0, 0.1], 'limegreen': [0.1, 1], 'orange': [1, 2], 'red': [2, 3]})
            ], style={'display': 'flex', 'justify-content': 'space-evenly', 'margin-top': '2px'}),
        html.Div(id='text_report1', style={'marginTop': '10px', 'whiteSpace': 'pre-wrap', 'text-align': 'justify', 'marginLeft': '50px', 'marginRight': '50px'}),
        ###
        # Void message (blank if not)
        ###
        html.Div(id='score_summary', style={'text-align': 'center', 'font-size': '24px', 'margin-top': '30px'}),
        html.Br(),
        html.Hr(className='orange_line')
    ]),
    #############
    # SECTION 2 #
    #############
    html.Div([
        html.P(
            'Risk of exposure',
            style={
                'fontSize': '40px',
                'textAlign': 'center',
                'marginTop': '20px',
                'marginBottom': '20px',
                'fontWeight': 'bold'  # optional: makes it more prominent
            }
        ),
        html.Div([
            build_gauge('gauge2', 0.05, {'grey': [0, 0.1], 'limegreen': [0.1, 1], 'orange': [1, 2], 'red': [2, 3]})
            ], style={'display': 'flex', 'justify-content': 'space-evenly', 'margin-top': '40px'}),
        html.Div(id='text_report2', style={'marginTop': '50px', 'whiteSpace': 'pre-wrap', 'text-align': 'justify', 'marginLeft': '50px', 'marginRight': '50px'}),
        html.Br(),
        html.Hr(className='orange_line'),
    ]),
    #############
    # SECTION 3 #
    #############
    html.Div([
        html.P(
            'Individual preventive behaviours',
            style={
                'fontSize': '40px',
                'textAlign': 'center',
                'marginTop': '20px',
                'marginBottom': '20px',
                'fontWeight': 'bold'  # optional: makes it more prominent
            }
        ),
        html.Div([
            build_gauge('gauge3', 0.05, {'grey': [0, 0.1], 'red': [0.1, 1], 'orange': [1, 2], 'limegreen': [2, 3]})
            ], style={'display': 'flex', 'justify-content': 'space-evenly', 'margin-top': '40px'}),
        html.Div(id='text_report3', style={'marginTop': '50px', 'whiteSpace': 'pre-wrap', 'text-align': 'justify', 'marginLeft': '50px', 'marginRight': '50px'}),
        html.Br()
        #html.Hr(className='orange_line'),
    ]),
    ###############
    # PET SECTION #
    ###############
    html.Div(
        id='pet_advices',
        children=[
            html.Div(
                id='text_pet_advices',
                style={
                    'marginTop': '50px',
                    'whiteSpace': 'pre-wrap',
                    'text-align': 'justify',
                    'marginLeft': '50px',
                    'marginRight': '50px'
                }
            )       
        ]
    ),        
    ##################################
    # Gain confidence and conclusion #
    ##################################
    html.Div([
        html.Hr(className='orange_line'),
        html.P(
             'Gaining confidence with ticks',
             style={
                 'fontSize': '40px',
                 'textAlign': 'center',
                 'marginTop': '20px',
                 'marginBottom': '20px',
                 'fontWeight': 'bold'
             }
        ),
        dcc.Markdown("* Confidence in preventing tick bites will increase with the consistent implementation of tick preventive behaviours and experience. No method of tick bite prevention is 100% effective, and despite your best efforts, you may still find ticks on yourself, family members and pets. This does not mean you are doing something wrong!\n\n* Finding ticks is not always easy. Nymphs may be especially difficult to detect as they can be the size of a poppy seed. Again, practice and experience will help. If you are not physically able to detect a tick (e.g., due to poor eyesight or restricted movement), mirrors and a magnifying glass can make it easier, or if possible, asking someone to help.\n\n* Understandably, some people do not feel confident removing an attached tick. Common concerns include tick mouthparts being left in the skin or incorrect handling of the tick. For information on how to remove a tick and what not to do, check [TickTool] (https://ticktool.etick.ca/what-should-i-do-if-i-find-a-tick/).\n\n", style={'marginTop': '50px', 'whiteSpace': 'pre-wrap', 'text-align': 'justify', 'marginLeft': '50px', 'marginRight': '50px'}),      
        html.Hr(className='orange_line'),
        html.P(
             'Conclusion',
             style={
                 'fontSize': '40px',
                 'textAlign': 'center',
                 'marginTop': '20px',
                 'marginBottom': '20px',
                 'fontWeight': 'bold'
             }
        ),
        dcc.Markdown("We hope this report is helpful to you and enables you to feel more prepared and confident when spending time outdoors. Do you have any suggestions on how to improve the overall usefulness and user experience of this questionnaire? If so, please send your ideas to [pratique-ticktool@medvet.umontreal.ca](mailto:pratique-ticktool@medvet.umontreal.ca), we would love to hear them. For more information on ticks and tick-borne diseases in Canada, you can consult the following resources: \n\n [Government of Canada] (https://www.canada.ca/en/public-health/services/diseases/ticks-tick-borne-diseases.html)\n\n [TickTool] (https://ticktool.etick.ca/)\n\n", style={'marginTop': '50px', 'whiteSpace': 'pre-wrap', 'text-align': 'justify', 'marginLeft': '50px', 'marginRight': '50px'})
    ]),
    #####################
    # Export the report #
    #####################
    html.Div(
        [
            dcc.Link(
                'Revise my questionnaire',
                href='/page-2',
                className='modern-link',
                style={
                    'display': 'inline-block',
                    'textAlign': 'center',
                    'backgroundColor': '#FF9636',
                    'color': 'white',
                    'padding': '10px',
                    'fontSize': '15px',
                    'borderRadius': '5px',
                    'textDecoration': 'none',
                    'whiteSpace': 'nowrap',
                    'height': '42px',  # match button height
                    'lineHeight': '22px'  # vertical alignment fix
                }
            ),
            html.Button(
                'Export my report to a PDF document',
                id='print-button',
                n_clicks=0,
                style={
                    'width': '300px',
                    'textAlign': 'center',
                    'backgroundColor': '#FF9636',
                    'border': 'none',
                    'borderRadius': '5px',
                    'padding': '10px',
                    'fontSize': '15px',
                    'cursor': 'pointer',
                    'color': 'white',
                    'whiteSpace': 'nowrap',
                    'height': '42px',
                }
            ),
        ],
        style={
            'display': 'flex',
            'justifyContent': 'center',
            'alignItems': 'center',
            'gap': '40px',
            'marginTop': '20px'
        }
    ),
    html.Br(),
    html.Hr(className='grey_blue_line'),
    ####################
    # Risk Calculation #
    ####################
    html.Div(
    [
        html.P("To learn how your risk levels were calculated, please click here:", style={
            'margin': '0',
            'paddingRight': '8px',
            'fontSize': '16px',
            'display': 'inline'
        }),
        dcc.Link('Methodology', href='/methodology', style={
            'fontSize': '20px',
            'display': 'inline',
            'color': 'blue',
            'textDecoration': 'underline'
        })
    ],
    style={
        'display': 'flex',
        'justifyContent': 'center',
        'alignItems': 'center',
        'marginTop': '30px'
    }
    ),
    html.Br(),
    html.Br(),
    html.Div(id='display-answers_p8', style={'marginTop': '50px', 'whiteSpace': 'pre-wrap'})
    
])
        
        
# CALLBACKS

@callback(
    Output('gauge1', 'figure'),
    Output('gauge2', 'figure'),
    Output('gauge3', 'figure'),
    Input('record_answers', 'data')
)



def calculat_score_and_record_answers(data):
    ######
    #Enregistrement des données en cas de consentement
    ######
    try : 
        if data and data.get('consent') == 'yes':
            now = datetime.datetime.now()
            ip_address = request.remote_addr
            myline = str(ip_address) + '\t' + now.strftime('%Y-%m-%d %H:%M:%S') 
            for k in mykeys:
                if k in data.keys():
                    myline += '\t' + str(data[k])
                else:
                    myline += '\t\t'
               
            myline += '\n'
            unique_output = re.sub(r'[^a-zA-Z0-9]', '_', now.strftime('%Y-%m-%d %H:%M:%S'))
            filename = 'survey_results_' +  unique_output + '.tsv'
            with open(filename, 'a') as tsvfile:
                tsvfile.write(myline)
    except:
        pass
    ######
    ######
    # Evaluation score1 BLT in environment
    ######
    score1 = 0.05
    try :
        if data and 'zipcode' in data:
            risk = risk_dict.get(data['zipcode'], 'Unknown')
            if risk == 'High':
                score1 = 2.4
            elif risk == 'Medium':
                if data['How_many_embedded_in_your_skin'] != "Not applicable" \
                    and data['How_many_embedded_in_your_skin'] != "I don't remember" \
                        and data['How_many_embedded_in_your_skin'] != "0" \
                            and data['How_many_freely_moving_on_your_skin'] != "Not applicable" \
                                and data['How_many_freely_moving_on_your_skin'] != "I don't remember" \
                                    and data['How_many_freely_moving_on_your_skin'] != "0":
                                score1 = 2.4
                else:
                    if data['access_courtyard'] == "Yes" :
                        if(data['courtyard_herbaceous_or_forest'] == 'Yes'):
                            score1 = 2.4
                        else:
                            if data['house_deer'] == "Yes":
                                score1 = 2.4
                            else:
                                if data['house_proximity_wooded_area'] == "Yes":
                                    score1 = 2.4
                                else :
                                    score1 = 1.5
                    else:
                        if data['house_proximity_wooded_area'] == "Yes":
                            score1 = 2.4
                        else:
                            score1 = 1.5
            elif risk == 'Low':
                if ( (data['How_many_embedded_in_your_skin'] != "Not applicable") \
                    and (data['How_many_embedded_in_your_skin'] != "I don't remember") \
                        and (data['How_many_embedded_in_your_skin'] != "0")):
                    score1 = 1.5
                else:
                    if data['access_courtyard'] == "Yes" :
                        if data['house_deer'] == "Yes":
                            score1 = 1.5
                        else:
                            if data['house_proximity_wooded_area'] == "Yes":
                                score1 = 1.5
    except :
        pass
    ######
    # Risk of exposure
    #######       
    score2 = 0.05
    # optimiser avec x not in list
    try :
        if data['How_many_embedded_in_your_skin'] != "Not applicable" \
            and data['How_many_embedded_in_your_skin'] != "I don't remember" \
                and data['How_many_embedded_in_your_skin'] != "0"\
                    and data['How_many_freely_moving_on_your_skin'] != "Not applicable" \
                        and data['How_many_freely_moving_on_your_skin'] != "I don't remember" \
                            and data['How_many_freely_moving_on_your_skin'] != "0":
                        score2 = 2.4
        else:
            if data['frequency_outdoor_activities'] == 'Very often (More than 10 times a year)':
                score2 = 2.4
            else:
                if ( data['time_daily_wooded_area'] == 'Between one and five hours per day' ) or (  data['time_daily_wooded_area'] == 'More than five hours per day' ):
                    score2 = 2.4
                else:
                    if data['frequency_outdoor_activities'] == 'Rarely':
                        score2 = 1.5
                    else:
                        if data['time_daily_wooded_area'] in {'Never', 'Less than one hour per day'}:
                            score2 =1.5
    except :
        pass
    ######
    # Preventive behavior
    #######
    score3 = 0.05
    ###
    try :
        # Constructuion d'une table de reponses considérées comme oui
        considered_as_yes = ['Most of the time', 'Always', 'Not applicable to my situation']
        # Calcul du score de mesures de protection
        score_at_least_4_protective_behaviours = 0
        if data['search_for_informations_ticks'] == 'yes' :
            score_at_least_4_protective_behaviours += 1
        if data['Wearing_long_layers_of_clothing'] in considered_as_yes :
            score_at_least_4_protective_behaviours += 1
        if data['Wearing_light-coloured_clothing'] in considered_as_yes :
            score_at_least_4_protective_behaviours += 1
        if data['Tucking_in_clothes'] in considered_as_yes :
            score_at_least_4_protective_behaviours += 1
        if data['DEET'] in considered_as_yes :
            score_at_least_4_protective_behaviours += 1
        if data['Walking_on_cleared_paths'] in considered_as_yes :
            score_at_least_4_protective_behaviours += 1
        if data['Examining_your_clothes'] in considered_as_yes :
            score_at_least_4_protective_behaviours += 1
        if data['clothes_in_the_dryer'] in considered_as_yes :
            score_at_least_4_protective_behaviours += 1
        if data['Bathing_or_showering'] in considered_as_yes :
            score_at_least_4_protective_behaviours += 1
        ######
        ######
        risk = risk_dict.get(data['zipcode'], 'Unknown')
        if (risk == 'High') or (risk == 'Medium') or (data['visite_area_disease_ticks'] == 'yes') : 
            if data['Examining_yourself'] == 'Most of the time' or data['Examining_yourself'] == 'Always':
                if (risk == 'Medium') or (risk == 'High'):
                    if data['access_courtyard'] == 'yes':
                        if data['courtyard_mowing'] in considered_as_yes:
                            if data['courtyard_fallen_leaves'] in considered_as_yes:
                                if data['courtyard_clearing_herbaceous'] in considered_as_yes:
                                    if data['courtyard_clearing_herbaceous'] in considered_as_yes:
                                        if data['courtyard_fences_deer'] in considered_as_yes:
                                            if score_at_least_4_protective_behaviours >= 4 :
                                                score3 = 2.4
                                            else :
                                                score3  = 1.5
                                        else :
                                            if score_at_least_4_protective_behaviours >= 4 :
                                                score3 = 1.5
                                            else:
                                                score3 = 0.6
                                else :
                                    if score_at_least_4_protective_behaviours >= 4 :
                                        score3 = 1.5
                                    else :
                                        score3 = 0.6
                            else :
                                score3 = 0.6
                        else :
                            score3 = 0.6
                    else:
                        if score_at_least_4_protective_behaviours >= 4:
                            score3 = 2.4
                        else :
                            score3 = 1.5
                else :
                    if score_at_least_4_protective_behaviours >= 4:
                        score3 = 2.4  
                    else :
                        score3 = 1.5
            else :
                score3 = 0.6
    except :
        pass
    ######
    ######
    ######
    ######
    fig1 = build_gauge_figure(score1, {'grey': [0, 0.1], 'limegreen': [0.1, 1], 'orange': [1, 2], 'red': [2, 3]})
    fig2 = build_gauge_figure(score2, {'grey': [0, 0.1], 'limegreen': [0.1, 1], 'orange': [1, 2], 'red': [2, 3]})
    fig3 = build_gauge_figure(score3, {'grey': [0, 0.1], 'red': [0.1, 1], 'orange': [1, 2], 'limegreen': [2, 3]})
    

    return fig1, fig2, fig3


# def calculat_score_and_record_answers(data):
#     ######
#     #Enregistrement des données en cas de consentement
#     ######
#     if data and data.get('consent') == 'yes':
#         now = datetime.datetime.now()
#         ip_address = request.remote_addr
#         myline = str(ip_address) + '\t' + now.strftime('%Y-%m-%d %H:%M:%S') 
#         for k in mykeys:
#             if k in data.keys():
#                 myline += '\t' + str(data[k])
#             else:
#                 myline += '\t\t'
           
#         myline += '\n'
#         unique_output = re.sub(r'[^a-zA-Z0-9]', '_', now.strftime('%Y-%m-%d %H:%M:%S'))
#         filename = 'survey_results_' +  unique_output + '.tsv'
#         with open(filename, 'a') as tsvfile:
#             tsvfile.write(myline)
#     ######
#     ######
#     # Risk Calculation based on zipcode
#     #zipcode = data['zipcode']
#     risk = risk_dict.get(data['zipcode'], 'Unknown')
#     ######
#     ######
#     # Evaluation score1 BLT in environment
#     ######
#     score1 = 0
#     if data and 'zipcode' in data:
#         if risk == 'High':
#             score1 = 2.4
#         elif risk == 'Medium':
#             if data['How_many_embedded_in_your_skin'] != "Not applicable" \
#                 and data['How_many_embedded_in_your_skin'] != "I don't remember" \
#                     and data['How_many_embedded_in_your_skin'] != "0" \
#                         and data['How_many_freely_moving_on_your_skin'] != "Not applicable" \
#                             and data['How_many_freely_moving_on_your_skin'] != "I don't remember" \
#                                 and data['How_many_freely_moving_on_your_skin'] != "0":
#                             score1 = 2.4
#             else:
#                 if data['access_courtyard'] == "Yes" :
#                     if(data['courtyard_herbaceous_or_forest'] == 'Yes'):
#                         score1 = 2.4
#                     else:
#                         if data['house_deer'] == "Yes":
#                             score1 = 2.4
#                         else:
#                             if data['house_proximity_wooded_area'] == "Yes":
#                                 score1 = 2.4
#                             else :
#                                 score1 = 1.5
#                 else:
#                     if data['house_proximity_wooded_area'] == "Yes":
#                         score1 = 2.4
#                     else:
#                         score1 = 1.5
#         elif risk == 'Low':
#             if ( (data['How_many_embedded_in_your_skin'] != "Not applicable") \
#                 and (data['How_many_embedded_in_your_skin'] != "I don't remember") \
#                     and (data['How_many_embedded_in_your_skin'] != "0")):
#                 score1 = 1.5
#             else:
#                 if data['access_courtyard'] == "Yes" :
#                     if data['house_deer'] == "Yes":
#                         score1 = 1.5
#                     else:
#                         if data['house_proximity_wooded_area'] == "Yes":
#                             score1 = 1.5
#         #elif risk not found !
#     ######
#     # Risk of exposure
#     #######       
#     score2 = 0
#     # optimiser avec x not in list
#     if data['How_many_embedded_in_your_skin'] != "Not applicable" \
#         and data['How_many_embedded_in_your_skin'] != "I don't remember" \
#             and data['How_many_embedded_in_your_skin'] != "0"\
#                 and data['How_many_freely_moving_on_your_skin'] != "Not applicable" \
#                     and data['How_many_freely_moving_on_your_skin'] != "I don't remember" \
#                         and data['How_many_freely_moving_on_your_skin'] != "0":
#                     score2 = 2.4
#     else:
#         if data['frequency_outdoor_activities'] == 'Very often (More than 10 times a year)':
#             score2 = 2.4
#         else:
#             if ( data['time_daily_wooded_area'] == 'Between one and five hours per day' ) or (  data['time_daily_wooded_area'] == 'More than five hours per day' ):
#                 score2 = 2.4
#             else:
#                 if data['frequency_outdoor_activities'] == 'Rarely':
#                     score2 = 1.5
#                 else:
#                     if data['time_daily_wooded_area'] in {'Never', 'Less than one hour per day'}:
#                         score2 =1.5
#     ######
#     # Preventive behavior
#     #######
#     score3 = 0
#     ###
#     # Constructuion d'une table de reponses considérées comme oui
#     considered_as_yes = ['Most of the time', 'Always', 'Not applicable to my situation']
#     # Calcul du score de mesures de protection
#     score_at_least_4_protective_behaviours = 0
#     if data['search_for_informations_ticks'] == 'yes' :
#         score_at_least_4_protective_behaviours += 1
#     if data['Wearing_long_layers_of_clothing'] in considered_as_yes :
#         score_at_least_4_protective_behaviours += 1
#     if data['Wearing_light-coloured_clothing'] in considered_as_yes :
#         score_at_least_4_protective_behaviours += 1
#     if data['Tucking_in_clothes'] in considered_as_yes :
#         score_at_least_4_protective_behaviours += 1
#     if data['DEET'] in considered_as_yes :
#         score_at_least_4_protective_behaviours += 1
#     if data['Walking_on_cleared_paths'] in considered_as_yes :
#         score_at_least_4_protective_behaviours += 1
#     if data['Examining_your_clothes'] in considered_as_yes :
#         score_at_least_4_protective_behaviours += 1
#     if data['clothes_in_the_dryer'] in considered_as_yes :
#         score_at_least_4_protective_behaviours += 1
#     if data['Bathing_or_showering'] in considered_as_yes :
#         score_at_least_4_protective_behaviours += 1
#     ######
#     ######
#     if (risk == 'High') or (risk == 'Medium') or (data['visite_area_disease_ticks'] == 'yes') : 
#         if data['Examining_yourself'] == 'Most of the time' or data['Examining_yourself'] == 'Always':
#             if (risk == 'Medium') or (risk == 'High'):
#                 if data['access_courtyard'] == 'yes':
#                     if data['courtyard_mowing'] in considered_as_yes:
#                         if data['courtyard_fallen_leaves'] in considered_as_yes:
#                             if data['courtyard_clearing_herbaceous'] in considered_as_yes:
#                                 if data['courtyard_clearing_herbaceous'] in considered_as_yes:
#                                     if data['courtyard_fences_deer'] in considered_as_yes:
#                                         if score_at_least_4_protective_behaviours >= 4 :
#                                             score3 = 2.4
#                                         else :
#                                             score3  = 1.5
#                                     else :
#                                         if score_at_least_4_protective_behaviours >= 4 :
#                                             score3 = 1.5
#                                         else:
#                                             score3 = 0.6
#                             else :
#                                 if score_at_least_4_protective_behaviours >= 4 :
#                                     score3 = 1.5
#                                 else :
#                                     score3 = 0.6
#                         else :
#                             score3 = 0.6
#                     else :
#                         score3 = 0.6
#                 else:
#                     if score_at_least_4_protective_behaviours >= 4:
#                         score3 = 2.4
#                     else :
#                         score3 = 1.5
#             else :
#                 if score_at_least_4_protective_behaviours >= 4:
#                     score3 = 2.4  
#                 else :
#                     score3 = 1.5
#         else :
#             score3 = 0.6
#     ######
#     ######
#     ######
#     ######
#     return score1, score2, score3


######
# Adaptated text report
######

# @callback(
#     Output('score_summary', 'children'),
#     Input('computed_scores', 'data')
# )
# def update_summary(scores):
#     if scores is None:
#         return "Waiting for scores..."

#     messages = []

#     if scores['score1'] >= 2:
#         messages.append("Risk 1 is high.")
#     elif scores['score1'] >= 1:
#         messages.append("Risk 1 is moderate.")
#     else:
#         messages.append("Risk 1 is low.")

#     if scores['score2'] >= 2:
#         messages.append("Risk 2 is high.")
#     elif scores['score2'] >= 1:
#         messages.append("Risk 2 is moderate.")
#     else:
#         messages.append("Risk 2 is low.")

#     if scores['score3'] >= 2:
#         messages.append("Risk 3 is high.")
#     elif scores['score3'] >= 1:
#         messages.append("Risk 3 is moderate.")
#     else:
#         messages.append("Risk 3 is low.")

#     return html.Ul([html.Li(msg) for msg in messages])
# @callback(
#     Output('text_no_calculation1', 'children'),
#     Input('computed_scores', 'data')
#     )

# def display_no_calculation(scores):
#     print(scores)
#     if scores is None:
#         return "Waiting for scores..."
#     sentence = 'PLATE !'
#     return dcc.Markdown(sentence)
   


#   return sentence

@callback(
    Output('text_report_1', 'children'),
    Input('record_answers', 'data')
    )

def display_personalized_text1(data):
    
    risk = risk_dict.get(data['zipcode'], 'Unknown')
    no_anti_ticks = ['no', 'yes', "I don't remember"]
    
    ###############################################################################
    # 1 The potential presence of blacklegged ticks in your environment
    ###############################################################################
    
    sentence = ''
    
    #Postal Code & residency feedback
    if data['which_residence'] == 'Primary' or data['which_residence'] == 'Secondary':
        sentence += f"""* The region of your {data['which_residence']} residence has a **{risk}** level risk"""
    else :
        sentence += f"""* The region of your residence has a **{risk}** level risk"""
    
    sentence += '\n\n'
    
    #Blacklegged ticks on your property and property management
    sentence += "* Evidence suggests that most tick exposure occurs in the peri-domestic environment, rather than further afield. While it is not possible to determine your exact level of risk for blacklegged ticks based on a questionnaire, the presence of certain features on or near your property can provide an indication of risk, based on evidence reported in the scientific literature.\n\n"
    
    # Herbaceous or wooded area in proximity
    if data['house_proximity_wooded_area'] not in no_anti_ticks:
        sentence += "* You reported having **herbaceous or wooded areas or edges on your property, and/or living near a wooded area**. The presence of herbaceous, wooded areas, and the intersection of these two habitats have been shown to be associated with an increase in diseases spread by ticks. This does not mean that you cannot spend time outdoors, but rather that **you should be vigilant and take steps to protect yourself**. There are several ways you can reduce the risk of exposure to ticks on your property - for more information, check [What can I do to reduce ticks in my yard?] (https://ticktool.etick.ca/what-can-i-do-to-reduce-ticks-in-my-yard/). Remember to protect yourself while making modification to your property by **wearing long clothes and applying bug repellent, and to perform a tick check and take a bath or shower afterwards**.\n"
    
    # Courtyard feedback
    if data['access_courtyard']== 'yes':
        sentence += "* You reported **having a courtyard, garden, or wooded area**. While having an outdoor space does not automatically mean you are at risk of tick exposure, there are certain elements which are known to increase your risk of tick bite and/or diseases spread by ticks. These include: The **size of your yard, Certain types of cover, such as flower or vegetable gardens and herbaceous and wooded areas**.The **presence of a wood pile, the presence of a stone wall, the presence of leaf litter Activity areas such as children’s play areas, dining areas, and sitting areas**.\n"
    
    #children's play equipment
    if data['courtyard_children_play_area'] == 'yes':
        sentence += "* You reported **having children’s play equipment or an activity structure on your property**. It is a good idea to **move this type of equipment closer to the house, and away from long grass or herbaceous/wooded areas**. It is **preferable to have wood chips rather than grass in this area, or to keep the grass very short**.\n\n"
    
    
    #deer on your property
    if data['house_deer'] == 'yes':
        sentence += "* You reported **seeing or suspecting deer on your property**. Deer are a host species for the blacklegged tick, meaning they play an important role in the life cycle of the tick. Research suggests that not having a fence to exclude deer is associated with an increased risk of tick bites, and that the presence of deer is associated with an increased risk for people getting a disease spread by ticks. While it may not be feasible to install fencing around the entirety of your property, you could consider fencing off an area of the property that you use regularly. Doing this will also prevent deer from eating your plants and provides a safe space for pets to run. There are several ways you can reduce the risk of exposure to ticks on your property, such as installing fences and creating a mulch or gravel border around your yard. For more information, check [What can I do to reduce ticks in my yard?] (https://ticktool.etick.ca/what-can-i-do-to-reduce-ticks-in-my-yard/). Remember to protect yourself while working on your property by wearing long clothes and applying bug repellent, and to perform a tick check and take a bath or shower afterwards.\n\n"
   
    sentence += '\n\n\n\n'
    
    return dcc.Markdown(sentence)

#######
#######

@callback(
    Output('text_report2', 'children'),
    Input('record_answers', 'data')
    )

def display_personalized_text2(data):
    
    
    sentence = ""
    
    #Your tick exposure in the last 12 months
    #sentence += "### Your tick exposure in the last 12 months\n\n"
    
    try :
    
        if (data['attached_to_your_skin'] != 'Never' and  data['attached_to_your_skin'] != 'Not applicable') or (data['Freely_moving'] != 'Never' and  data['Freely_moving'] != 'Not applicable'):
            sentence += "* You reported having found a tick on yourself in the last 12 months. For this reason, you have been given a ‘high’ risk level for tick exposure.\n\n"
    except :
        pass
    
    try :
        if data['On_a_pet'] != 'Never' and  data['On_a_pet'] != 'Not applicable':
            sentence += "* You reported having found a tick on your pet in the last 12 months. For this reason, you have been given a ‘high’ risk level for tick exposure, as pet exposure to ticks usually suggests that their owners have also been in at at-risk habitat.\n\n"
    except :
        pass
    
    try :
        if data['Freely_moving_outside'] != 'Never' and  data['Freely_moving_outside'] != 'Not applicable':
            sentence += "* You reported having found a tick in your environment in the last 12 months. For this reason, you have been given a ‘high’ risk level for tick exposure as this suggests you spend time in or near tick habitats.\n\n"
    except :
        pass
    
    
    #outdoor activity
    try :
        
        if data['time_daily_wooded_area'] == 'More than five hours per day':
            sentence += "* You reported engaging in at least one outdoor activity which occurs in potential tick habitats, at least once or twice a season. Outdoor recreation in general can be associated with increased tick bites and risk of disease spread by ticks, and increased time spent in vegetation can also increase the risk of diseases spread by ticks. Previous research studies have found associations between specific activities such as hiking, hunting, and yard work and an increased risk of contracting a disease transmitted by ticks. However, it is prudent to assume that there can be a risk of tick exposure when participating in any outdoor activity occurring in grassy, wooded, or herbaceous areas. While there is no need to stop doing these activities – it is important to protect yourself, your family, and your pets from tick bites, and to always perform tick checks! \n\n"
        elif data['time_daily_wooded_area'] == 'Between one and five hours per day':
            sentence += "* As with engaging in outdoor activities, occupational exposure to ticks has been associated with an increased risk of diseases spread by ticks, therefore it is important for you to adopt consistent and regular prevention measures. Depending on the bug repellent you choose to use and how long you are outdoors in one day, you may need to reapply the repellent while you are outside, so take it with you and/or leave one in the car. It is also a good idea to stop and perform tick checks throughout the day, rather than waiting until the end of the day.\n\n"
    except :
        pass
        
    try :
        if data['time_daily_wooded_area'] == 'More than five hours per day' or data['time_daily_wooded_area'] == 'Between one and five hours per day':
            sentence += "* If you frequently work or spend time in potential tick habitats, you may wish to invest in clothing which has been treated with permethrin as an additional layer of protection. For more information on how to protect yourself from ticks when outdoors, check [Everything you need to know about prevention] (https://ticktool.etick.ca/all-you-need-to-know-about-ticks/)\n\n"
    except :
        pass    
    no_in_prior_tick_exposure = ['Never','Not applicable']
    
    try :
        if (data['time_daily_wooded_area'] == 'Never' or data['time_daily_wooded_area'] == 'Less than one hour per day') \
            and (data['attached_to_your_skin'] in no_in_prior_tick_exposure ) \
                and (data['Freely_moving'] in no_in_prior_tick_exposure ) \
                    and (data['On_a_pet'] in no_in_prior_tick_exposure) \
                        and (data['Freely_moving_outside'] in no_in_prior_tick_exposure) :
                            sentence += "* You reported spending little time either recreating or working outdoors, meaning you are less likely to enter tick habitats. However, note that is a low risk of encountering a tick anywhere in Canada south of the Arctic circle due to the possibility of ticks being dispersed by birds outside of their usual habitats.\n\n"
        
        if (data['time_daily_wooded_area'] == 'Never' or data['time_daily_wooded_area'] == 'Less than one hour per day') \
            and ( (data['attached_to_your_skin'] not in no_in_prior_tick_exposure ) \
                or (data['Freely_moving'] not in no_in_prior_tick_exposure ) \
                    or (data['On_a_pet'] not in no_in_prior_tick_exposure) \
                        or (data['Freely_moving_outside'] not in no_in_prior_tick_exposure) ):
                            sentence += "* You reported having found a tick before, despite spending little time recreating or working outdoors. This may be because your activities bring you into proximity with tick habitats or that you encountered a tick outside of its usual habitat. Regardless of why, it will be important to remain vigilant and to perform tick checks.\n\n"
    except :
        pass   
    return dcc.Markdown(sentence)

#######
#######

@callback(
    Output('text_report3', 'children'),
    Input('record_answers', 'data')
    )

def display_personalized_text3(data):
    
    sentence = ""
    
    # try :
    #     risk = risk_dict.get(data['zipcode'], 'Unknown')
    #     if risk == 'Low':
    #         sentence += "*This is the risk level you would be given if you lived in or visited a Lyme disease risk area, or if Lyme disease emerges in your current region.*\n\n"
    # except:
    #     sentence += "*This is the risk level you would be given if you lived in or visited a Lyme disease risk area, or if Lyme disease emerges in your current region.*\n\n"
        
    sentence += "Research has demonstrated the association between increased risk of diseases spread by ticks and the lack of adopting protective measures, including not performing a tick check, not using bug repellent, not wearing appropriate clothing, and not bathing after spending time outdoors. Each behaviour provides an additional layer of protection, and there is no single behaviour which is guaranteed to prevent tick bites or disease. Therefore, it is recommended that you adopt as many preventive behaviours as is possible and feasible for you and your family : [TickTool link](https://ticktool.etick.ca/incorporate-prevention) \n\n"
    
    no_body_check = ['Never','Rarely', 'Sometimes']
    try :
        if data['Examining_yourself'] in no_body_check:
            sentence += "* You reported that you never, rarely, or sometimes perform a body check for ticks after being in a wooded area in a Lyme disease endemic region, which is why you have received a ‘Low’ score for your preventive behaviours.\n\n"
    
        if data['Examining_yourself'] in no_body_check or data['Examining_yourself'] == 'Not applicable':
            sentence += "* While no single behaviour has consistently been demonstrated to be the most effective, performing a thorough tick check is the most widely recommended method of protection. It does not require special equipment - although a full-length and hand-held mirror can help – it just takes time. By planning ahead and scheduling 10 minutes for a tick check after spending time outdoors, you can make it more likely that you will do so, and thereby reduce your chance of a tick bite or getting a disease spread by ticks. And don’t forget to check other household members and pets too! If you find a tick, congratulate yourself on doing so, remove it and continue your tick check in case there are more\n\n"
        else :
            sentence += "* You reported that you perform a body check for ticks most of the time after being in a wooded area in a Lyme disease endemic region – well done! While no single behaviour has consistently been demonstrated to be the most effective, performing a tick check is the most widely recommended method of protection you can adopt. It does not require special equipment - although a full-length and hand-held mirror can help – it just takes time. By planning ahead and scheduling time for a tick check after spending time outdoors, you can make it more likely that you will do so, and thereby reduce your chance of a tick bite or getting a disease spread by ticks. And don’t forget to check other household members and pets too! If you find a tick, congratulate yourself on doing so, remove it and continue your tick check in case there are more.\n\n"
    except :
        pass   
    
    #Q13 ????????
    
    # Living alone or live with someone feedback
    try:
        if data['live_alone'] == 'yes' :
            sentence += """* Performing tick checks can be challenging for everyone, as ticks like to hide in places where they cannot be found. As you **live alone**, it can be very useful to have both a **full-length mirror** as well as a **handheld mirror** to make this process easier.Some people find that having a **lint roller** available can help to reach ticks which have not attached, and similarly, a **loofah in the shower** can help to dislodge ticks from places you cannot reach. Remember to pay particular attention to your **scalp, hairline, ears, arms, chest, back, waist, belly button, groin, legs and behind knees, and between the toes**.\n\n  In 2021, 45% of Lyme disease cases in Canada were diagnosed in adults aged 55-79 years. This does not mean that people in this age group cannot spend time outdoors, but rather suggests that this age group should **adopt consistent behaviours** to protect themselves from ticks.\n\n  For more information on how to protect yourself, check [Everything you need to know about prevention] (https://ticktool.etick.ca/all-you-need-to-know-about-ticks/)\n"""
        elif data['live_with_someone_over_18'] == 'yes' :
            sentence += """* As you **live with another adult**, you can **remind each other to adopt preventive behaviours** against tick bites and **help each other to perform a tick check** – particularly the hard-to-reach places such as the **scalp and back**. By helping and reminding each other to think about ticks, it will be **easier to incorporate these practices into your routine**.**If performing a tick check alone**, it can be very useful to have both a **full-length mirror** as well as a **handheld mirror** to make this process easier. Some people find that having a **lint roller** available can also be helpful to reach ticks which have not attached, and similarly, a **loofah in the shower** can help to dislodge ticks from places you cannot reach.\n\n  In 2021, 45% of Lyme disease cases in Canada were diagnosed in adults aged 55-79 years. This does not mean that people in this age group cannot spend time outdoors, but rather suggests that this age group should try to adopt consistent behaviours to protect themselves from ticks.\n\n  For more information on how to protect yourself, check [Everything you need to know about prevention] (https://ticktool.etick.ca/all-you-need-to-know-about-ticks/)\n"""
        elif data['live_with_child_0_4'] == 'yes' or data['live_with_child_5_14'] == 'yes' or data['live_with_child_15_18'] == 'yes':
            sentence += """* Approximately **11% of Lyme disease cases reported in Canada in 2021 were in children aged 5-14 years**, however other evidence suggests that the risk of tick bites is **higher in children aged 5 years or less**. This can be attributed to the fact that children this age **often play low to the ground and leave designated trails**. They are also **less likely to check themselves** for ticks. This does **not** mean that older children cannot develop a tick-borne disease, and it is important for all members of the family to learn how to protect themselves from ticks. As with adults, the risk can be reduced by performing a **tick check, wearing long clothes, tucking in clothes, wearing bug repellent if over 6 months of age, and bathing or showering after spending time outdoors**.\n  For more information on how to protect children from ticks bites, check [How can I protect my children?] (https://ticktool.etick.ca/how-can-i-protect-my-children/)’.\n"""
    except :
        pass
    
    try :
    #Lawn management practice
        #sentence += "\n\nThere are several ways to reduce the risk of tick exposure of your property. Here, we will describe three key methods:\n\n"
        
        yes_property_management = ['Most of the time', 'Always']
        
        #Mowing
        if data['courtyard_mowing'] in yes_property_management:
            sentence += "* Well done for regularly maintaining the lawn! Keeping the grass short is very important in reducing the risk of tick exposure. Ticks climb up long grass so they can attach to people and animals who brush past. By regularly and consistently keeping the grass short – especially in areas which you or your pets access – you are making your property less hospitable for ticks.\n\n"
        else:
            sentence += "* Lawn maintenance is very important in reducing the risk of tick exposure. Ticks climb up long grass so they can attach to people and animals who brush past. By regularly and consistently keeping the grass short – especially in areas which you or your pets access – you can make your property less hospitable for ticks.\n\n"
        
        #Removing leaves
        if data['courtyard_fallen_leaves'] in yes_property_management:
            sentence += "* Well done for regularly removing leaves on your property! Leaf litter provides a safe environment for ticks, keeping them warm in the winter and preventing them from drying out in the summer. By removing leaf litter, you are reducing one of the most important habitats for ticks in your property. Depending on the size of you property, you may wish to focus on the areas you or your pets like to spend time in.n\n"
        else:
            sentence += "* Leaf litter provides a safe environment for ticks, keeping them warm in the winter and preventing them from drying out in the summer. By removing leaf litter, you can reduce one of the most important habitats for ticks in your property. Depending on the size of you property, you may wish to focus on the areas you or your pets like to spend time in.\n\n"
        
        #Brush and branches
        if data['courtyard_clearing_herbaceous'] in yes_property_management:
            sentence += "* Well done for regularly clearing herbaceous brush and trimming branches! These habitats provide a suitable environment for small rodents, which not only carry ticks but are vital in the life cycle of the bacteria which cause Lyme disease and other diseases spread by ticks. By removing herbaceous areas in the areas where you or your pets spend a lot of time, you are making these areas less hospitable for mice and ticks, reducing the chance of them venturing close to your house.\n\n"
        else :
            sentence += "* Herbaceous brush and long branches provide a suitable environment for small rodents, which not only carry ticks but are vital in the life cycle of the bacteria which cause Lyme disease and other diseases spread by ticks. By removing herbaceous areas in the areas where you or your pets spend a lot of time, you can make these areas less hospitable for mice and ticks, reducing the chance of them venturing close to your house.\n\n"
        
        sentence += "Bear in mind that yard work, time spent in vegetation and general outdoor activity can increase your risk of getting a disease spread by ticks, so remember to protect yourself while working on your property by wearing long clothes and applying bug repellent, and to perform a tick check and take a bath or shower afterwards. Many people are concerned outdoor measures to reduce the risk of tick exposure may have negative environmental consequence. To learn more about this and other FAQs, check ‘[What can I do to reduce ticks in my yard?] (https://ticktool.etick.ca/what-can-i-do-to-reduce-ticks-in-my-yard/).\n\n"
     
    except :
        pass
     
    return dcc.Markdown(sentence)

#######
#######

@callback(
    Output(component_id='pet_advices', component_property='hidden'),
    Input('record_answers', 'data')
    )

def display_pet_advices(data):
    if data['dog'] == 'yes' or data['cat'] == 'yes' or data['horse'] == 'yes':
        return False
    else:
        return True


@callback(
    Output('text_pet_advices', 'children'),
    Input('record_answers', 'data')
    )

def display_personalized_pet_advices_text(data):
    
    sentence = ''
    
    no_anti_ticks = ['no', "I don't remember"]
    
    #Dog anti-tick treatnment
    if data['dog'] == 'yes' or data['cat'] == 'yes' or data['horse'] == 'yes':
        sentence += "* Pets are **not able to transmit Lyme disease or other tick-borne diseases to humans. Having a pet has been associated with an increased risk of tick bites or disease spread by ticks. This is usually because having a pet means you spend more time outdoors and therefore closer to ticks**. It does not mean you should avoid having pets! If you see ticks on your pet, this suggests that you may also have been in a tick habitat and that you should take steps to protect both you, your pet(s), and your family.\n\n"
    
    if data['anti_tick_treatment_dog'] in no_anti_ticks :
        sentence += "* You reported **taking care of at least one dog**. Dogs are at risk for tick bites, and **just like people, can suffer from Lyme disease** and other diseases transmitted by ticks.  Fortunately, there are several species-specific products available for pets to protect them from ticks and Lyme disease, including **tablets, spot-on treatments, and vaccines**. Some of these products can also protect your pet from other parasites such as **fleas and worms**. Your veterinarian is the best person to advise you on these options so you can choose what is right for you to use, and when, based on your activities and risk, local climate, efficacy of available preventive medications, and your own preferences. There is no evidence to suggest that having a dog increases your risk of getting a disease spread by ticks. However, **people who have dogs may spend more time outdoors** in tick habitats, so it is important for you to protect yourself from ticks.\n\n"
    elif data['anti_tick_treatment_dog'] == 'yes':
        sentence += "* You reported **taking care of at least one dog and providing them with anti-tick products** – well done! Dogs are at risk for tick bites, and **just like people, can suffer from Lyme disease** and other diseases transmitted by ticks. By administering a tick preventive product, you are helping to keeping them safe. There are several species-specific products available for pets to protect them from ticks and Lyme disease, including **tablets, spot-on treatments, and vaccines**. Some of these products can also protect your pet from other parasites such as **fleas and worms**. Your veterinarian is the best person to advise you on these options so you can choose what is right for you to use, and when, based on your activities and risk, local climate, efficacy of available preventive medications, and your own preferences. There is no evidence to suggest that having a dog increases your risk of getting a disease spread by ticks. However, **people who have dogs may spend more time outdoors** in tick habitats, so it is important for you to protect yourself from ticks.\n\n"
    
    #Cats anti-tick treatments 
    if data['anti_tick_treatment_cat'] in no_anti_ticks :
        sentence += "* You reported taking care of at least one cat. Cats are at risk for tick bites, so it is important to protect them with species-specific tick preventive products. By administering a tick preventive product, you are helping to keeping them safe. There are several **species-specific products** available for pets to protect them from ticks, including tablets and spot-on treatments. Some of these products can also protect your pet from other parasites such as fleas and worms. Your veterinarian is the best person to advise you on these options so you can choose what is right for you to use, and when, based on your activities and risk, local climate, efficacy of available preventive medications, and your own preferences. Interestingly, cat ownership has been associated with an increased risk of diseases spread by ticks, whereas this has not been found with dog ownership.  This may be due to differences in preventive behaviours between cat and dog owners, differences in administration of tick preventive products, reduced tick checks in cats, increased grooming behaviour in cats or because cats are more likely to roam in long grass. Regardless of why this association has been found, it is always advisable to perform tick checks on your cat, if possible, and to speak to your veterinarian about tick prevention measures.\n\n"
    elif  data['anti_tick_treatment_cat'] == 'yes':
        sentence += "* You reported taking care of at least one cat and providing them with anti-tick products – well done!  Cats are at risk for tick bites, so it is important to protect them with species-specific tick preventive products. There are several **species-specific products** available for pets to protect them from ticks, including tablets and spot-on treatments. Some of these products can also protect your pet from other parasites such as fleas and worms. Your veterinarian is the best person to advise you on these options so you can choose what is right for you to use, and when, based on your activities and risk, local climate, efficacy of available preventive medications, and your own preferences. Interestingly, cat ownership has been associated with an increased risk of diseases spread by ticks, whereas this has not been found with dog ownership.  This may be due to differences in preventive behaviours between cat and dog owners, differences in administration of tick preventive products, reduced tick checks in cats, increased grooming behaviour in cats or because cats are more likely to roam in long grass. Regardless of why this association has been found, it is always advisable to perform tick checks on your cat, if possible, and to speak to your veterinarian about tick prevention measures.\n\n"   
    #Horse
    if data['horse'] == 'yes':
        sentence += "* Horses can suffer from Lyme disease too, and as there is no vaccine licensed for horses, tick prevention is important. Grooming and checking for ticks daily, appropriate pasture management, and the use of species-specific bug repellents can all help to reduce the risk of tick bites. For more information on diseases spread by ticks and tick bite prevention, speak to your veterinarian. Some studies have found that owning or riding horses has been associated with an increased risk of tick bites and disease spread by ticks. This is most likely due to riders and horses being in the same environment and having a similar risk of tick exposure.\n"
    
    sentence += "* For more information on pets and ticks, visit [How can I protect my pets?](https://ticktool.etick.ca/how-can-i-protect-my-pets/)    [Tick Talk Canada]( https://ticktalkcanada.com/)\n\n"
    
    # return [html.Hr(className='orange_line'),
    #     html.P(
    #         'A note about pets',
    #         style={
    #             'fontSize': '40px',
    #             'textAlign': 'center',
    #             'marginTop': '20px',
    #             'marginBottom': '20px',
    #             'fontWeight': 'bold'
    #         }
    #     ),
    #     dcc.Mardown(sentence)]
    return html.Div([
        html.Hr(className='orange_line'),
        html.P(
            'A note about pets',
            style={
                'fontSize': '40px',
                'textAlign': 'center',
                'marginTop': '20px',
                'marginBottom': '20px',
                'fontWeight': 'bold'
            }
        ),
        dcc.Markdown(sentence)
    ])




#### Print the dictionnary

# @callback(
#     Output('hidden-div', 'children'),
#     Input('print-button', 'n_clicks')
# )
# def trigger_print(n_clicks):
#     if n_clicks > 0:
#         return dcc.Location(id='print-location', href='javascript:window.print();')
#     return ''

# ######
# ######

# #Display data dictionnary for dev
   
# @callback(
#     Output('display-answers_p8', 'children'),
#     Input('record_answers', 'data')
# )

# def display_answers_p8(data):
#     if data:
#         return html.Pre(json.dumps(data, indent=2))
#     return "No data recorded yet."
