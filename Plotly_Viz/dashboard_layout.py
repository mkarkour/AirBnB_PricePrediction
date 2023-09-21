from dash import html, dcc


def generate_layout(df):
    return html.Div(children=[
        html.H1('Data Cleaning & Analysis'),
        dcc.Graph(
            id='graph1'),
        html.Div(children=[
            html.Div([
                html.Label('Data Source'),
                dcc.Dropdown(
                    id='data-source',
                    options=[
                        {'label': 'Raw dataset', 'value': 'raw'},
                        {'label': 'Cleaned dataset', 'value': 'cleaned'}
                    ],
                    value='raw'
                )
            ],
                style={'width': '33%', 'display': 'inline-block'}),
            html.Div([
                html.Label('Parameter to plot'),
                dcc.Dropdown(
                    id='data-dropdown',
                    options=[{'label': col, 'value': col}
                             for col in df.columns],
                    value='realSum'
                )
            ],
                style={'width': '33%', 'display': 'inline-block'}),
            html.Div([
                html.Label('Type of Plot'),
                dcc.Dropdown(
                    id='plot-dropdown',
                    options=[{'label': 'Histogram', 'value': 'histogram'},
                             {'label': 'Violin', 'value': 'violin'}],
                    value='histogram'
                )
            ],
                style={'width': '33%', 'display': 'inline-block'})
        ]),
        dcc.Graph(
            id='graph2',
        ),
        html.Div(children=[
            html.Div([
                html.Label('Type of Plot'),
                dcc.Dropdown(
                    id='x-scatter',
                    options=[{'label': col, 'value': col}
                             for col in df.columns],
                    value=df.columns[0]
                )
            ],
                style={'width': '25%', 'display': 'inline-block'}),
            html.Div([
                html.Label('Type of Plot'),
                dcc.Dropdown(
                    id='y-scatter',
                    options=[{'label': col, 'value': col}
                             for col in df.columns],
                    value=df.columns[1] 
                )
            ],
                style={'width': '25%', 'display': 'inline-block'})
        ]),
        dcc.Graph(
            id='graph3',
        ),
    ])
