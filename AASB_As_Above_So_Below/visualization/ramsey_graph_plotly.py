# visualization/ramsey_graph_plotly.py

import plotly.graph_objects as go
import numpy as np
from itertools import combinations

# Define the main forces with their properties
FORCES = [
    {"name": "Forex", "category": "Direct", "angle": 0},
    {"name": "Bond Yields", "category": "Direct", "angle": 30},
    {"name": "Derivatives", "category": "Direct", "angle": 60},
    {"name": "Stock Indices", "category": "Direct", "angle": 90},
    {"name": "Interest Rates", "category": "Direct", "angle": 120},
    {"name": "Commodity Prices", "category": "Direct", "angle": 150},
    {"name": "Geopolitical Events", "category": "Indirect", "angle": 180},
    {"name": "Climate Patterns", "category": "Indirect", "angle": 210},
    {"name": "Cultural Trends", "category": "Indirect", "angle": 240},
    {"name": "Social Media Trends", "category": "Indirect", "angle": 270},
    {"name": "Technological Innovations", "category": "Indirect", "angle": 300},
    {"name": "Global Consciousness Project", "category": "Indirect", "angle": 330}
]

# Define sub-forces for each main force (example data)
SUB_FORCES = {
    "Forex": [
        {"name": "Currency Reserves", "category": "Direct", "angle": 0},
        {"name": "Exchange Policies", "category": "Direct", "angle": 30},
        {"name": "Market Liquidity", "category": "Direct", "angle": 60},
        {"name": "Interest Rate Differentials", "category": "Direct", "angle": 90},
        {"name": "Trade Balances", "category": "Direct", "angle": 120},
        {"name": "Political Stability", "category": "Direct", "angle": 150},
        {"name": "Economic Indicators", "category": "Indirect", "angle": 180},
        {"name": "Inflation Rates", "category": "Indirect", "angle": 210},
        {"name": "Fiscal Policies", "category": "Indirect", "angle": 240},
        {"name": "Monetary Policies", "category": "Indirect", "angle": 270},
        {"name": "Global Events", "category": "Indirect", "angle": 300},
        {"name": "Speculative Trading", "category": "Indirect", "angle": 330}
    ],
    "Bond Yields": [
        {"name": "Government Bonds", "category": "Direct", "angle": 0},
        {"name": "Corporate Bonds", "category": "Direct", "angle": 30},
        {"name": "Municipal Bonds", "category": "Direct", "angle": 60},
        {"name": "High-Yield Bonds", "category": "Direct", "angle": 90},
        {"name": "Inflation-Indexed Bonds", "category": "Direct", "angle": 120},
        {"name": "Convertible Bonds", "category": "Direct", "angle": 150},
        {"name": "Credit Ratings", "category": "Indirect", "angle": 180},
        {"name": "Interest Rate Forecasts", "category": "Indirect", "angle": 210},
        {"name": "Economic Growth", "category": "Indirect", "angle": 240},
        {"name": "Government Fiscal Health", "category": "Indirect", "angle": 270},
        {"name": "Investor Sentiment", "category": "Indirect", "angle": 300},
        {"name": "Global Economic Trends", "category": "Indirect", "angle": 330}
    ],
    # Add similar sub-forces for other main forces...
    # For brevity, only Forex and Bond Yields sub-forces are included here.
}

# Define color mapping for categories
CATEGORY_COLORS = {
    "Direct": "#1f77b4",    # Blue
    "Indirect": "#ff7f0e"   # Orange
}

def calculate_positions(forces, radius=1):
    """
    Calculate x and y positions for each force based on their angles.
    
    :param forces: List of dictionaries containing force information.
    :param radius: Radius of the circle on which forces are placed.
    :return: Two lists containing x and y coordinates.
    """
    angles_rad = [force["angle"] * np.pi / 180 for force in forces]
    x = [radius * np.cos(theta) for theta in angles_rad]
    y = [radius * np.sin(theta) for theta in angles_rad]
    return x, y

def create_ramsey_graph(forces):
    """
    Create a Plotly figure representing the Ramsey graph.
    
    :param forces: List of dictionaries containing force information.
    :return: Plotly Figure object.
    """
    n = len(forces)
    x, y = calculate_positions(forces)
    
    # Create edge traces
    edge_x = []
    edge_y = []
    for i, j in combinations(range(n), 2):
        # Example condition: connect all nodes (complete graph)
        edge_x += [x[i], x[j], None]
        edge_y += [y[i], y[j], None]
    
    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(width=1, color='gray'),
        hoverinfo='none',
        mode='lines'
    )
    
    # Create node traces
    node_x = x
    node_y = y
    node_text = [force["name"] for force in forces]
    node_color = [CATEGORY_COLORS[force["category"]] for force in forces]
    
    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode='markers+text',
        text=node_text,
        textposition="top center",
        marker=dict(
            showscale=False,
            color=node_color,
            size=20,
            line=dict(width=2, color='black')
        ),
        hoverinfo='text',
        customdata=node_text,
    )
    
    # Create figure
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title='Ramsey Graph: Macro Analysis',
                        titlefont_size=16,
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )
    
    # Add annotations for better clarity
    for idx, force in enumerate(forces):
        fig.add_annotation(
            x=x[idx],
            y=y[idx],
            text=force["name"],
            showarrow=False,
            font=dict(
                size=10,
                color="black"
            ),
            xanchor='center',
            yanchor='bottom'
        )
    
    # Update layout for aesthetics
    fig.update_layout(
        width=800,
        height=800,
        plot_bgcolor='white'
    )
    
    return fig

def create_sub_ramsey_graph(main_force_name, sub_forces):
    """
    Create a Plotly figure representing a sub Ramsey graph for a specific main force.
    
    :param main_force_name: Name of the main force.
    :param sub_forces: List of dictionaries containing sub-force information.
    :return: Plotly Figure object.
    """
    n = len(sub_forces)
    x, y = calculate_positions(sub_forces)
    
    # Create edge traces
    edge_x = []
    edge_y = []
    for i, j in combinations(range(n), 2):
        # Example condition: connect all nodes (complete graph)
        edge_x += [x[i], x[j], None]
        edge_y += [y[i], y[j], None]
    
    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(width=1, color='lightgray'),
        hoverinfo='none',
        mode='lines'
    )
    
    # Create node traces
    node_x = x
    node_y = y
    node_text = [force["name"] for force in sub_forces]
    node_color = [CATEGORY_COLORS[force["category"]] for force in sub_forces]
    
    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode='markers+text',
        text=node_text,
        textposition="top center",
        marker=dict(
            showscale=False,
            color=node_color,
            size=15,
            line=dict(width=2, color='black')
        ),
        hoverinfo='text',
        customdata=node_text,
    )
    
    # Create figure
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title=f'Ramsey Graph: {main_force_name} - Micro Analysis',
                        titlefont_size=16,
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )
    
    # Add annotations for better clarity
    for idx, force in enumerate(sub_forces):
        fig.add_annotation(
            x=x[idx],
            y=y[idx],
            text=force["name"],
            showarrow=False,
            font=dict(
                size=10,
                color="black"
            ),
            xanchor='center',
            yanchor='bottom'
        )
    
    # Update layout for aesthetics
    fig.update_layout(
        width=800,
        height=800,
        plot_bgcolor='white'
    )
    
    return fig
