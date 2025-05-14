import dash
from dash import html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import json

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Keyboard Layout Visualizer"),
    html.Div([
        html.Label("Enter layout configuration (JSON):"),
        dcc.Textarea(
            id='layout-input',
            value='[]',
            style={'width': '100%', 'height': '200px'}
        ),
    ]),
    html.Div([
        dcc.Graph(id='layout-graph')
    ])
])

@app.callback(
    Output('layout-graph', 'figure'),
    Input('layout-input', 'value')
)
def update_graph(layout_text):
    try:
        layout = json.loads(layout_text)
        df = pd.DataFrame(columns=['x', 'y', 'matrix'])
        
        for lay in layout:
            x = lay["x"]
            y = lay["y"]
            matrix = str(lay["matrix"])
            df = pd.concat([df, pd.DataFrame({"x":[x], "y":[y], "matrix":[matrix]})], ignore_index=True)
        
        # Invert both x and y axes to rotate 180 degrees
        df['x'] = -df['x']
        df['y'] = -df['y']
        
        fig = px.scatter(df, x='x', y='y', text='matrix')
        fig.update_traces(textposition='top center')
        fig.update_layout(
            title="Keyboard Layout (180° Rotated)",
            xaxis_title="X Position",
            yaxis_title="Y Position",
            showlegend=False
        )
        return fig
    except Exception as e:
        # Return empty figure if there's an error
        return px.scatter()

if __name__ == '__main__':
    app.run_server(debug=True) 