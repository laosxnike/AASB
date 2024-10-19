# visualization/visualize_recursive_graph.py

from .ramsey_graph_plotly import create_ramsey_graph, create_sub_ramsey_graph, FORCES, SUB_FORCES
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go

# Initialize the Dash app
app = dash.Dash(__name__)
app.title = "Ramsey Graph Visualization"

# Create the main Ramsey graph figure
main_fig = create_ramsey_graph(FORCES)

app.layout = html.Div([
    html.H1("Ramsey Graph: Macro Analysis", style={'textAlign': 'center'}),
    dcc.Graph(
        id='ramsey-graph',
        figure=main_fig,
        config={'displayModeBar': False},
        style={'height': '800px'}
    ),
    html.Div(id='graph-title', style={'textAlign': 'center', 'fontSize': 24, 'marginTop': 20}),
    html.Button("Back", id='back-button', n_clicks=0, style={'display': 'none', 'margin': '0 auto', 'display': 'block'}),
    dcc.Store(id='navigation-history', data=[])
], style={'width': '80%', 'margin': '0 auto'})

@app.callback(
    [
        Output('ramsey-graph', 'figure'),
        Output('graph-title', 'children'),
        Output('back-button', 'style'),
        Output('navigation-history', 'data')
    ],
    [
        Input('ramsey-graph', 'clickData'),
        Input('back-button', 'n_clicks')
    ],
    [
        State('navigation-history', 'data')
    ]
)
def update_graph(clickData, back_clicks, history):
    ctx = dash.callback_context

    if not ctx.triggered:
        trigger_id = 'No clicks yet'
    else:
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # If "Back" button is clicked
    if trigger_id == 'back-button' and history:
        # Remove the last entry from history
        history.pop()
        
        if not history:
            # If history is empty, show the main graph
            fig = main_fig
            title = "Ramsey Graph: Macro Analysis"
            back_button_style = {'display': 'none', 'margin': '0 auto', 'display': 'block'}
        else:
            # Get the previous graph details
            previous_force = history[-1]
            sub_fig = create_sub_ramsey_graph(previous_force, SUB_FORCES[previous_force])
            fig = sub_fig
            title = f"Ramsey Graph: {previous_force} - Micro Analysis"
            back_button_style = {'display': 'block', 'margin': '0 auto', 'display': 'block'}
        
        return fig, title, back_button_style, history

    # If a node is clicked and we are on the main graph or navigating deeper
    elif trigger_id == 'ramsey-graph' and clickData:
        clicked_force = clickData['points'][0]['customdata']
        
        # Check if the clicked force has sub-forces defined
        if clicked_force in SUB_FORCES:
            # Update history
            history.append(clicked_force)
            
            # Create sub Ramsey graph
            sub_fig = create_sub_ramsey_graph(clicked_force, SUB_FORCES[clicked_force])
            title = f"Ramsey Graph: {clicked_force} - Micro Analysis"
            back_button_style = {'display': 'block', 'margin': '0 auto', 'display': 'block'}
            
            return sub_fig, title, back_button_style, history

    # Default return (main graph)
    return main_fig, "Ramsey Graph: Macro Analysis", {'display': 'none'}, []

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
