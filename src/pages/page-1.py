#!/usr/bin/env python3
# Import packages

import dash
from dash import dcc, html, Input, Output, callback, State
import random
import plotly.graph_objs as go
import uuid
import logging

dash.register_page(__name__, path='/')

# Configuration
allowed_values = [0.1, 0.6, 1.5, 2.4]
step_size = 0.05
pause_ticks = 20

def get_initial_state():
    return {
        "session_id": str(uuid.uuid4()),
        "gauge_in1": {"current": 0.0, "target": 0.6, "wait": 0, "has_left_zero": False},
        "gauge_in2": {"current": 0.0, "target": 1.5, "wait": 0, "has_left_zero": False},
        "gauge_in3": {"current": 0.0, "target": 2.4, "wait": 0, "has_left_zero": False},
    }

def build_gauge(gauge_id, value, color_ranges, tickvals, ticktext):
    # Ensure value is within valid range
    value = max(0, min(3, float(value)))
    
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
    
    # Simplified update_traces to avoid potential issues
    fig.update_traces(value=value)
    
    # Set layout config for better deployment compatibility
    fig.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),
        autosize=True,
        font=dict(family="Arial, sans-serif")
    )
    
    return dcc.Graph(
        id=gauge_id, 
        figure=fig, 
        style={'height': '500px', 'width': '500px'},
        config={
            'displayModeBar': False,
            'staticPlot': False,
            'responsive': True
        }
    )

layout = html.Div([
    html.Img(src='/assets/TickTOOL_logo.png', style={'width': '40%', 'height': '40%'}, className='image-gallery'),
    html.Hr(className='orange_line'),
    html.Br(),

    html.Div([
        html.Div([
            html.B('Evaluate your prevention strategy', style={'font-size': '60px'})
        ], style={'textAlign': 'center'}),
        html.Br(),
        html.Br(),
    
        html.P([
            "The potential risk from tick bites – and how to prevent tick bites – can sometimes feel a little overwhelming. ",
            "Would you like to better understand your risk of being bitten by a tick and learn how to improve your tick bite prevention strategy for yourself and your family? ",
            "Complete the questionnaire and receive a personalised report so you can make informed decisions and take action in a way that is right for you, to help keep you and your family safe."
        ], style={
            'textAlign': 'justify',
            'marginLeft': '20px',
            'marginRight': '20px',
            'fontSize': '20px'
        }),
    
        html.Br(), html.Br(),
    
        html.P(
            "The questionnaire should take approximately 10 minutes to complete. "
            "Your personalized report will show three levels of risk: one based on how likely it is to find blacklegged ticks in your area, "
            "one based on your outdoor activities, and one based on the behaviours you adopt to protect yourself — as shown below.",
            style={
                'textAlign': 'justify',
                'marginLeft': '20px',
                'marginRight': '20px',
                'fontSize': '20px'
            }
    )
    ]),

    html.Br(),
    html.Div([
        html.Div([
            html.P('Potential for blacklegged ticks in environment', style={'font-size': '25px', "font-weight": "bold", 'textAlign': 'center'}),
            build_gauge('gauge_in1', 0.0, {
                'grey': [0, 0.1], 'limegreen': [0.1, 1], 'orange': [1, 2], 'red': [2, 3]
            }, [0.6, 1.5, 2.4], ['Low', 'Moderate', 'High'])
        ], style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'}),
    
        html.Div([
            html.P('Risk of exposure', style={'font-size': '25px', "font-weight": "bold", 'textAlign': 'center'}),
            build_gauge('gauge_in2', 0.0, {
                'grey': [0, 0.1], 'limegreen': [0.1, 1], 'orange': [1, 2], 'red': [2, 3]
            }, [0.6, 1.5, 2.4], ['Low', 'Moderate', 'High'])
        ], style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'}),
    
        html.Div([
            html.P('Level of preventive behaviours', style={'font-size': '25px', "font-weight": "bold", 'textAlign': 'center'}),
            build_gauge('gauge_in3', 0.0, {
                'grey': [0, 0.1], 'red': [0.1, 1], 'orange': [1, 2], 'limegreen': [2, 3]
            }, [0.6, 1.5, 2.4], ['Low', 'Moderate', 'High'])
        ], style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'})
    ], style={
        'display': 'flex',
        'justifyContent': 'space-evenly',
        'alignItems': 'flex-start',
        'marginTop': '40px'
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
    
    # Initialize state store with suppress_callback_exceptions compatibility
    dcc.Store(id='gauge-state', data=get_initial_state(), storage_type='memory'),
    
    # Single interval with longer interval for server deployment
    dcc.Interval(
        id='interval-component', 
        interval=200,  # Increased interval for server stability
        n_intervals=0, 
        disabled=False,
        max_intervals=-1  # Run indefinitely
    ),
    
    # Hidden div to store animation status for debugging
    html.Div(id='animation-status', style={'display': 'none'}),
])

def update_gauge_value(gauge_data):
    """Update function for individual gauge values"""
    try:
        current = float(gauge_data.get("current", 0.0))
        target = float(gauge_data.get("target", 0.6))
        wait = int(gauge_data.get("wait", 0))
        has_left_zero = bool(gauge_data.get("has_left_zero", False))

        if wait > 0:
            return {
                "current": current, 
                "target": target, 
                "wait": wait - 1, 
                "has_left_zero": has_left_zero
            }

        if abs(current - target) < step_size:
            if not has_left_zero and target > 0:
                has_left_zero = True
            
            # Select new target
            possible_values = [v for v in allowed_values if v != target and (has_left_zero or v > 0)]
            if not possible_values:
                possible_values = [v for v in allowed_values if v != target]
            
            new_target = random.choice(possible_values) if possible_values else target
            
            return {
                "current": round(target, 2), 
                "target": new_target, 
                "wait": pause_ticks, 
                "has_left_zero": has_left_zero
            }
        else:
            direction = 1 if target > current else -1
            new_current = current + direction * step_size
            new_current = max(0, min(3, round(new_current, 2)))  # Clamp to valid range
            
            return {
                "current": new_current, 
                "target": target, 
                "wait": 0, 
                "has_left_zero": has_left_zero
            }
    except Exception as e:
        logging.error(f"Error in update_gauge_value: {e}")
        return gauge_data  # Return unchanged data on error

def create_gauge_figure(current_value, color_ranges, tickvals, ticktext):
    """Create gauge figure with error handling"""
    try:
        current_value = max(0, min(3, float(current_value)))
        
        fig = go.Figure(go.Indicator(
            mode="gauge",
            value=current_value,
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
        
        fig.update_layout(
            margin=dict(l=20, r=20, t=20, b=20),
            autosize=True,
            font=dict(family="Arial, sans-serif"),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig
    except Exception as e:
        logging.error(f"Error creating gauge figure: {e}")
        # Return a basic figure on error
        return go.Figure()

# Simplified callback with better error handling
@callback(
    [Output('gauge_in1', 'figure'),
     Output('gauge_in2', 'figure'),
     Output('gauge_in3', 'figure'),
     Output('gauge-state', 'data'),
     Output('animation-status', 'children')],
    [Input('interval-component', 'n_intervals')],
    [State('gauge-state', 'data')],
    prevent_initial_call=False
)
def animate_gauges(n_intervals, state):
    try:
        # Initialize state if None or invalid
        if state is None or not isinstance(state, dict):
            state = get_initial_state()
            
        # Ensure all gauge data exists
        for gauge_key in ['gauge_in1', 'gauge_in2', 'gauge_in3']:
            if gauge_key not in state:
                state[gauge_key] = {"current": 0.0, "target": 0.6, "wait": 0, "has_left_zero": False}

        # Update each gauge
        updated_state = state.copy()
        updated_state["gauge_in1"] = update_gauge_value(state["gauge_in1"])
        updated_state["gauge_in2"] = update_gauge_value(state["gauge_in2"])
        updated_state["gauge_in3"] = update_gauge_value(state["gauge_in3"])

        # Create figures
        fig1 = create_gauge_figure(
            updated_state["gauge_in1"]["current"],
            {'grey': [0, 0.1], 'limegreen': [0.1, 1], 'orange': [1, 2], 'red': [2, 3]},
            [0.6, 1.5, 2.4], ['Low', 'Moderate', 'High']
        )

        fig2 = create_gauge_figure(
            updated_state["gauge_in2"]["current"],
            {'grey': [0, 0.1], 'limegreen': [0.1, 1], 'orange': [1, 2], 'red': [2, 3]},
            [0.6, 1.5, 2.4], ['Low', 'Moderate', 'High']
        )

        fig3 = create_gauge_figure(
            updated_state["gauge_in3"]["current"],
            {'grey': [0, 0.1], 'red': [0.1, 1], 'orange': [1, 2], 'limegreen': [2, 3]},
            [0.6, 1.5, 2.4], ['Low', 'Moderate', 'High']
        )

        status = f"Animation running - Interval: {n_intervals}"
        
        return fig1, fig2, fig3, updated_state, status

    except Exception as e:
        logging.error(f"Error in animate_gauges callback: {e}")
        
        # Fallback: return static gauges
        if state is None:
            state = get_initial_state()
        
        try:
            fig1 = create_gauge_figure(
                state.get("gauge_in1", {}).get("current", 0.0),
                {'grey': [0, 0.1], 'limegreen': [0.1, 1], 'orange': [1, 2], 'red': [2, 3]},
                [0.6, 1.5, 2.4], ['Low', 'Moderate', 'High']
            )

            fig2 = create_gauge_figure(
                state.get("gauge_in2", {}).get("current", 0.0),
                {'grey': [0, 0.1], 'limegreen': [0.1, 1], 'orange': [1, 2], 'red': [2, 3]},
                [0.6, 1.5, 2.4], ['Low', 'Moderate', 'High']
            )

            fig3 = create_gauge_figure(
                state.get("gauge_in3", {}).get("current", 0.0),
                {'grey': [0, 0.1], 'red': [0.1, 1], 'orange': [1, 2], 'limegreen': [2, 3]},
                [0.6, 1.5, 2.4], ['Low', 'Moderate', 'High']
            )

            return fig1, fig2, fig3, state, f"Error recovered: {str(e)[:100]}"
        
        except Exception as fallback_error:
            # Ultimate fallback
            empty_fig = go.Figure()
            return empty_fig, empty_fig, empty_fig, get_initial_state(), f"Critical error: {str(fallback_error)[:100]}"