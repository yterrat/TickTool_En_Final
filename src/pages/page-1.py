#!/usr/bin/env python3
# Import packages

import dash
from dash import dcc, html, Input, Output, callback, State
import random
import plotly.graph_objs as go
import time

dash.register_page(__name__, path='/')

# Configuration
allowed_values = [0.1, 0.6, 1.5, 2.4]
step_size = 0.05
pause_ticks = 20

# Server-side state storage (use Redis or database in production)
server_state = {
    "gauge_in1": {"current": 0.0, "target": 0.6, "wait": 0, "has_left_zero": False},
    "gauge_in2": {"current": 0.0, "target": 1.5, "wait": 0, "has_left_zero": False},
    "gauge_in3": {"current": 0.0, "target": 2.4, "wait": 0, "has_left_zero": False},
    "last_update": time.time()
}

def build_gauge(gauge_id, value, color_ranges, tickvals, ticktext):
    fig = go.Figure(go.Indicator(
        mode="gauge",
        value=value,
        gauge={
            'axis': {
                'range': [0, 3],
                'tickvals': tickvals,
                'ticktext': ticktext,
                'tickangle': 0,
                'tickfont': {'size': 18},
            },
            'bar': {'color': 'black', 'thickness': 0.2},
            'steps': [{'range': rng, 'color': clr} for clr, rng in color_ranges.items()],
        },
        domain={'x': [0, 1], 'y': [0, 1]},
        number={'valueformat': '.2f', 'font': {'color': 'rgba(0,0,0,0)'}}
    ))
    fig.update_traces(delta={'increasing': {'color': "green"}, 'decreasing': {'color': "red"}},
                      value=value)
    return dcc.Graph(id=gauge_id, figure=fig, style={'height': '500px', 'width': '500px'})

layout = html.Div([
    html.Img(src='/assets/TickTOOL_logo.png', style={'width': '40%', 'height': '40%'}, className='image-gallery'),
    html.Hr(className='orange_line'),
    html.Br(),
    html.Div([
        html.B('Evaluate your prevention strategy', style={'font-size': '60px'})
    ], style={'text-align': 'center'}),
    html.Br(),
    html.P([
        "The potential risk from tick bites - and how to prevent tick bites - can sometimes feel a little overwhelming",
        html.Br(),
        "Would you like to better understand your risk of being bitten by a tick and learn how to improve your tick bite prevention strategy for yourself and your family?",
        html.Br(), html.Br(),
        "Complete the questionnaire and receive a personalised report so you can make informed decisions and take action in a way that is right for you, to help keep you and your family safe.",
        html.Br(),
        "The questionnaire should take approximately 15 minutes to complete."
    ], style={'textAlign': 'center', 'marginLeft': '20px','marginRight': '20px','fontSize': '20px'}),

    html.Br(),
    html.Div([
        html.P('Potential for BLT in environment', style={'font-size': '25px', "font-weight": "bold"}),
        html.P('Risk of exposure', style={'font-size': '25px', "font-weight": "bold"}),
        html.P('Level of preventive behaviours', style={'font-size': '25px', "font-weight": "bold"})
    ], style={
        'display': 'flex',
        'justify-content': 'space-evenly',
        'align-items': 'center',
        'margin-top': '20px'
    }),

    html.Div([
        build_gauge('gauge_in1', 0.0, {
            'grey': [0, 0.1], 'limegreen': [0.1, 1], 'orange': [1, 2], 'red': [2, 3]
        }, [0.6, 1.5, 2.4], ['Low', 'Moderate', 'High']),

        build_gauge('gauge_in2', 0.0, {
            'grey': [0, 0.1], 'limegreen': [0.1, 1], 'orange': [1, 2], 'red': [2, 3]
        }, [0.6, 1.5, 2.4], ['Low', 'Moderate', 'High']),

        build_gauge('gauge_in3', 0.0, {
            'grey': [0, 0.1], 'red': [0.1, 1], 'orange': [1, 2], 'limegreen': [2, 3]
        }, [0.6, 1.5, 2.4], ['Low', 'Moderate', 'High'])
    ], style={
        'display': 'flex',
        'justify-content': 'space-evenly',
        'align-items': 'center',
        'margin-top': '40px',
    }),

    html.Br(),
    html.Div(dcc.Link("Begin the questionnaire and get your scores and personalized report", href='/page-2', style={
        'font-size': '20px',
        'text-decoration': 'none',
        'color': 'white',
        'background-color': '#FF9636',
        'padding': '10px 20px',
        'border-radius': '8px',
        'font-weight': '500',
        'display': 'inline-block'
    }), style={'text-align': 'center', 'margin-top': '30px'}),

    html.Br(), html.Br(),
    html.Img(src='/assets/UdeM.png', style={'width': '20%', 'height': '20%'}, className='image-gallery'),
    html.Br(), html.Br(),
    dcc.Interval(id='interval', interval=100, n_intervals=0)
])

@callback(
    Output('gauge_in1', 'figure'),
    Output('gauge_in2', 'figure'),
    Output('gauge_in3', 'figure'),
    Input('interval', 'n_intervals'),
    prevent_initial_call=True
)
def animate_gauges(n):
    global server_state
    
    def update_value(gauge_data):
        current = gauge_data["current"]
        target = gauge_data["target"]
        wait = gauge_data.get("wait", 0)
        has_left_zero = gauge_data.get("has_left_zero", False)

        if wait > 0:
            return {"current": current, "target": target, "wait": wait - 2, "has_left_zero": has_left_zero}

        if abs(current - target) < step_size:
            if not has_left_zero and target > 0:
                has_left_zero = True
            possible_values = [v for v in allowed_values if v != target and (has_left_zero or v > 0)]
            new_target = random.choice(possible_values)
            return {"current": round(target, 2), "target": new_target, "wait": pause_ticks, "has_left_zero": has_left_zero}
        else:
            direction = 1 if target > current else -1
            new_current = round(current + direction * step_size, 2)
            return {"current": new_current, "target": target, "wait": 0, "has_left_zero": has_left_zero}

    # Update server state
    server_state["gauge_in1"] = update_value(server_state["gauge_in1"])
    server_state["gauge_in2"] = update_value(server_state["gauge_in2"])
    server_state["gauge_in3"] = update_value(server_state["gauge_in3"])
    server_state["last_update"] = time.time()

    fig1 = build_gauge('gauge_in1', server_state["gauge_in1"]["current"],
                       {'grey': [0, 0.1], 'limegreen': [0.1, 1], 'orange': [1, 2], 'red': [2, 3]},
                       [0.6, 1.5, 2.4], ['Low', 'Moderate', 'High']).figure

    fig2 = build_gauge('gauge_in2', server_state["gauge_in2"]["current"],
                       {'grey': [0, 0.1], 'limegreen': [0.1, 1], 'orange': [1, 2], 'red': [2, 3]},
                       [0.6, 1.5, 2.4], ['Low', 'Moderate', 'High']).figure

    fig3 = build_gauge('gauge_in3', server_state["gauge_in3"]["current"],
                       {'grey': [0, 0.1], 'red': [0.1, 1], 'orange': [1, 2], 'limegreen': [2, 3]},
                       [0.6, 1.5, 2.4], ['Low', 'Moderate', 'High']).figure

    return fig1, fig2, fig3