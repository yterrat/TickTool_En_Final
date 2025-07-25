#!/usr/bin/env python3

# Import packages
import dash
from dash import dcc, html, Input, Output, callback, State
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/page-7')

layout = html.Div([
    html.Img(src='/assets/TickTOOL_logo.png', style={'width': '40%', 'height': '40%'}, className='image-gallery'),
    html.Hr(className='orange_line'),
    html.Br(),
    html.P("With your consent, the information you provide in this questionnaire may be used for research projects. \
           These projects will be under the responsibility of a principal investigator at the Université de Montréal \
           and will be authorized by a research ethics committee. \
           You will not be asked to provide your name or contact information. \
           The researcher undertakes to maintain and protect the confidentiality of the data concerning you, \
           under the conditions set out in this form. You may still complete the questionnaire and received a personalised report, even if you do not consent to your responses being used for research purposes.",
            style={"display":"flex", "gap":"1px", "align-items":"flex-end", 'font-size' : '20px', 'textAlign': 'justify'}),
    html.Br(),
    html.P("Consent for secondary use of data:",
           style={"display":"flex", "gap":"1px", "align-items":"flex-end", 'font-size' : '20px','text-decoration': 'underline'}),
    html.P("I consent to the researcher using, or authorizing students under their direction to use, \
           de-identified data for future research projects, conditional on their ethical \
               approval and in compliance with the same principles of confidentiality and protection of information.",
           style={"display":"flex", "gap":"1px", "align-items":"flex-end", 'font-size' : '20px'}),
    html.Br(),
    html.B("Do you consent to sharing your responses with l'Université de Montréal?", style={'font-size': '20px'}),
    html.Br(),
    html.Br(),
    html.Div([
        dcc.Dropdown(
            options=[
                {'label': 'Yes', 'value': 'yes'},
                {'label': 'No', 'value': 'no'}
            ],
            style={'width': '100px'},
            value='',
            id = 'consent'
        )
    ], style={'font-size': '15px', 'marginLeft' : '30px'}),
    html.Br(),
    html.Br(),
    #######
    #######
    
    html.Div(
        id='personal_questions',
        children=[
            html.Hr(className='grey_blue_line'),
            html.Br(),
            dcc.Markdown('*Thank you for agreeing to share your responses for research purposes. We would be grateful \
                   if you could complete the following socio-demographic questions. This information helps us direct \
                       Lyme disease educational material to where it is most useful. \
                           There is an ‘I prefer not to answer’ option for each question should you wish not to disclose this information.*',
                style={"display":"flex", "gap":"1px", "align-items":"flex-end", 'font-size' : '20px',}),
            html.Br(),
            html.Div([
                html.B('Socio-demographic questions', style={'font-size': '60px'})
                ], style={'text-align': 'center'}),
            ####
            ####
            html.P("What is your gender?", className='question_style2'),
            #Changre into ckeckbox
            html.Div([
                dcc.Dropdown(
                        options=[
                            {'label': 'Gender-fluid', 'value': 'Gender-fluid'},
                            {'label': "Man", 'value': "Man"},
                            {'label': "Non Binary", 'value': "NonBinary"},
                            {'label': "Trans Man", 'value': "Trans Man"},
                            {'label': "Trans Women", 'value': "Trans Women"},
                            {'label': "Two-spirit", 'value': "Two-spirit"},
                            {'label': "Women", 'value': "Women"},
                            {'label': "I don’t identify with any option provided ", 'value': "I don’t identify with any option provided "},
                            {'label': "I prefer not to answer ", 'value': "I prefer not to answer"}
                        ],
                        id='Gender',
                        value='I prefer not to answer'
                    )],
                    style={'font-size': '15px'}
                ),
            html.Br(),
            #html.Hr(className='grey_blue_line'),
            ######
            ######
            html.P("How old are you? ",  className='question_style2'),
            html.Div([
                dcc.Dropdown(
                        options=[
                            {'label': "Under 18", 'value': "Under 18"},
                            {'label': "Between 18-24", 'value': "18-24"},
                            {'label': "Between 25-34", 'value': "25-34"},
                            {'label': "Between 35-44", 'value': "35-44"},
                            {'label': "Between 45-54", 'value': "45-54"},
                            {'label': "Between 55-64", 'value': "55-64"},
                            {'label': "Between 65-74 ", 'value': "65-74"},
                            {'label': "75 or older", 'value': "75 or older"},
                            {'label': "I prefer not to answer", 'value': "I prefer not to answer"}
                        ],
                        id='Age',
                        value='I prefer not to answer'
                    )],
                    style={'font-size': '15px'}
                ),
            html.Br(),
            ##html.Hr(className='grey_blue_line'),
            ######
            ######
            html.P("What is the highest level of formal education that you have completed to date?", className='question_style2'),
            html.Div([
                dcc.Dropdown(
                        options=[
                            {'label': 'Elementary school or less', 'value': 'Elementary school or less'},
                            {'label': "Some post-secondary school", 'value': "Some post-secondary school"},
                            {'label': "College, vocational or trade school", 'value': "College, vocational or trade school"},
                            {'label': "Undergraduate university program", 'value': "Undergraduate university program"},
                            {'label': "Graduate or professional university program", 'value': "Graduate or professional university program"},
                            {'label': "I prefer not to answer", 'value': "I prefer not to answer"}
                        ],
                        id='Education',
                        value='I prefer not to answer'
                    )],
                    style={'font-size': '15px'}
                ),
            html.Br(),
            ##html.Hr(className='grey_blue_line'),
            ######
            ######
            html.P("Which of the following categories best describes your current employment status? ", className='question_style2'),
            html.Div([
                dcc.Dropdown(
                        options=[
                            {'label': 'Working full-time (35 or more hours per week)', 'value': 'Working full-time (35 or more hours per week)'},
                            {'label': 'Working part-time (less than 35 hours per week)', 'value': 'Working part-time (less than 35 hours per week)'},
                            {'label': "Self-employed", 'value': "Self-employed"},
                            {'label': "Student attending full time school (not working)", 'value': "Student attending full time school (not working)"},
                            {'label': "Unemployed, but looking for work", 'value': "Unemployed, but looking for work"},
                            {'label': "Not in the workforce (e.g. unemployed, but not looking for work, a full-time homemaker or parent)", 'value': "Not in the workforce (e.g. unemployed, but not looking for work, a full-time homemaker or parent), but looking for work"},
                            {'label': "Retired", 'value': "Retired"},
                            {'label': "Other", 'value': "Other"},
                            {'label': "I prefer not to answer", 'value': "I prefer not to answer"}
                        ],
                        id='Employment_status',
                        value='I prefer not to answer'
                        )],
                    style={'font-size': '15px'}
                ),
            html.Br(),
            ##html.Hr(className='grey_blue_line'),
            ######
            ######
            html.P("Which of the following categories best describes your total household income? That is, the total income of all persons in your household, before taxes?", className='question_style2'),
            html.Div([
                dcc.Dropdown(
                        options=[
                            {'label': 'Under $20,000', 'value': 'Under $20,000'},
                            {'label': "$20,000 to just under $40,000", 'value': "$20,000 to just under $40,000"},
                            {'label': "$40,000 to just under $60,000", 'value': "$40,000 to just under $60,000"},
                            {'label': "$60,000 to just under $80,000", 'value': "$60,000 to just under $80,000"},
                            {'label': "$80,000 to just under $100,000", 'value': "$80,000 to just under $100,000"},
                            {'label': "$100,000 to just under $120,000", 'value': "$100,000 to just under $120,000"},
                            {'label': "$120,000 to just under $150,000", 'value': "$120,000 to just under $150,000"},
                            {'label': "$150,000 and above", 'value': "$150,000 and above"},
                            {'label': "I prefer not to answer ", 'value': "I prefer not to answer"}
                        ],
                        id='Income',
                        value='I prefer not to answer'
                        )],
                    style={'font-size': '15px'}
                ),
            html.Br(),
            ##html.Hr(className='grey_blue_line'),
            html.P("What is the primary language spoken in your household?", className='question_style2'),
            html.Div([
                dcc.Dropdown(
                        options=[
                            {'label': 'English', 'value': 'English'},
                            {'label': "French", 'value': "French"},
                            {'label': "Other (please specify)", 'value': "Other (please specify)"},
                            {'label': "I prefer not to answer ", 'value': "I prefer not to answer"},
                        ],
                        id='primary_language',
                        value='I prefer not to answer'
                        )],
                        style={'font-size': '15px'}
                    ),
            html.Br(),
            #html.Hr(className='grey_blue_line'),
            ######
            ######
            html.P("Please select the population group(s) you identify with.", className='question_style2'),
            html.Div([
                dcc.Dropdown(
                        options=[
                            {'label': 'Arab', 'value': 'Arab'},
                            {'label': "Black", 'value': "Black"},
                            {'label': "Chinese", 'value': "Chinese"},
                            {'label': "Filipino", 'value': "Filipino"},
                            {'label': "Indigenous (that is, First Nation, Métis, or Inuk)", 'value': "Indigenous (that is, First Nation, Métis, or Inuk)"},
                            {'label': "Japanese", 'value': "Japanese"},
                            {'label': "Korean", 'value': "Korean"},
                            {'label': "Latin American", 'value': "Latin American"},
                            {'label': "South Asian (e.g., East Indian, Pakistani, Sri Lankan, etc.)", 'value': "South Asian (e.g., East Indian, Pakistani, Sri Lankan, etc.)"},
                            {'label': "Southeast Asian (including Vietnamese, Cambodian, Laotian, Thai, etc.)", 'value': "Southeast Asian (including Vietnamese, Cambodian, Laotian, Thai, etc.)"},
                            {'label': "West Asian (e.g., Iranian, Afghan, etc.)", 'value': "West Asian (e.g., Iranian, Afghan, etc.)"},
                            {'label': "White", 'value': "White"},
                            {'label': "Population group not listed above", 'value': "Population group not listed above"},
                            {'label': "I prefer not to answer", 'value': "I prefer not to answer"}
                        ],
                        id='population_group',
                        value='I prefer not to answer'
                        )],
                        style={'font-size': '15px'}
                    ),
            html.Div(
                id='population_group_addition',
                children=[
                    html.Br(),
                    html.P('Please specify the population group :',className='question_style2'),
                    dcc.Textarea(
                        id='population_group_text',
                        value='',
                        style={'width': '30%', 'height': 40}
                        )
                    ]),
            html.Br(),
            #html.Hr(className='grey_blue_line'),
            html.P("You have now completed the questionnaire! Thank you for your interest. If you would like to comment on your experience of completing the questionnaire, or on any of its content, please do so here:", className='question_style2'),
            dcc.Textarea(
                id='commentaries',
                value='',
                style={'width': '100%', 'height': 300}
        ),
    ]),
    html.Br(),
    html.Br(),
    #html.P("To access your personalised exposure profile report, please click 'Submit'.", style={'font-size' : '20px', "font-weight": "bold"}),
    html.Div(
    [
        dcc.Link(
            'Previous',
            href='/page-6',
            className='modern-link',
            style={'textAlign': 'center', 'whiteSpace': 'nowrap'}
        ),
        dcc.Link(
            'Access your personalized report',
            href='/page-8',
            className='modern-link',
            style={'textAlign': 'center', 'whiteSpace': 'nowrap'}
        ),
    ],
    style={
        'display': 'flex',
        'justifyContent': 'center',
        'alignItems': 'center',
        'gap': '40px'
        }
    ),
    #dcc.Link('Submit', href='/page-8', style={'font-size': '20px'}),
    html.Br(),
    html.Br(),
    dbc.Progress(value=100, style={"height": "15px"}, className="mb-3", label = "100% done"),
])
    
    
    


@callback(
    Output('record_answers', 'data',  allow_duplicate=True),
    Input('consent', 'value'),
    Input('Gender', 'value'),
    Input('Age', 'value'),
    Input('Education', 'value'),
    Input('Employment_status', 'value'),
    Input('Income', 'value'),
    Input('primary_language', 'value'),
    Input('population_group', 'value'),
    Input('population_group_text', 'value'),
    Input('commentaries', 'value'),
    State('record_answers', 'data'),
    prevent_initial_call=True,
)

def update_dic_p7(Q1,Q2,Q3,Q4,Q5,Q6,Q7,Q8,Q9,Q10,data):
    data = data or {}
    if Q1 is not None :
        data['consent'] = Q1
    if Q2 is not None :
        data['Gender'] = Q2
    if Q3 is not None :
        data['Age'] = Q3
    if Q4 is not None :
        data['Education'] = Q4
    if Q5 is not None :
        data['Employment_status'] = Q5
    if Q6 is not None :
        data['Income'] = Q6
    if Q7 is not None :
        data['primary_language'] = Q7
    if Q8 is not None :
        data['population_group'] = Q8
    if Q9 is not None:
        data['population_group_text'] = Q9
    if Q10 is not None :
        data['commentaries'] = Q10
    return data


# Afficher les valeurs du data quand la page esr reparcourue 

@callback(
    Output('consent', 'value'),
    Output('Gender', 'value'),
    Output('Age', 'value'),
    Output('Education', 'value'),
    Output('Employment_status', 'value'),
    Output('Income', 'value'),
    Output('primary_language', 'value'),
    Output('population_group', 'value'),
    Output('population_group_text', 'value'),
    Output('commentaries', 'value'),
    Input('record_answers', 'data')
)

def set_dropdown_value(data):
    return (
        data.get('consent', None),
        data.get('Gender', None),
        data.get('Age', None),
        data.get('Education', None),
        data.get('Employment_status', None),
        data.get('Income', None),
        data.get('primary_language', None),
        data.get('population_group', None),
        data.get('population_group_text', None),
        data.get('commentaries', None)
    )


@callback(
    Output(component_id='personal_questions', component_property='hidden'),
    [Input(component_id='consent', component_property='value')])

def show_hide_element_consent(consent):
    if consent == 'yes':
        return False
    else:
        return True
    
#######
#######
    
@callback(
    Output(component_id='population_group_addition', component_property='hidden'),
    [Input(component_id='population_group', component_property='value')])

def show_hide_element_population_group_addition(answ):
    if answ == 'Population group not listed above':
        return False
    else:
        return True

# @callback(
#     [Output('Age', 'value'),
#      Output('Education', 'value'),
#      Output('Employment_status', 'value'),
#      Output('Income', 'value'),
#      Output('primary_language', 'value'),
#      Output('population_group', 'value'),
#      Output('commentaries', 'value')
#     ],
#     Input('url', 'pathname'),
#     State('record_answers', 'data')
# )
  
# def initialize_inputs_page7(pathname, data):
#     if not data:
#         return [None, None]
#     return [
#      data.get('Age', None),
#      data.get('Education', None),
#      data.get('Employment_status', None),
#      data.get('Income', None),
#      data.get('primary_language', None),
#      data.get('population_group', None),
#      data.get('commentaries', None)
#      ]
         
