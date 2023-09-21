import dash
from dash.dependencies import Input, Output
import plotly.express as px
from dashboard_layout import generate_layout
from data_cleaning import clean_data
from raw_data_vizualisation import combine_city



df_raw = combine_city(["paris", "rome", "london", 'barcelona',
                      "athens", "berlin", "lisbon", "budapest", "vienna", "amsterdam"])

df_cleaned = clean_data(df_raw)

raw_data_columns = ["week_time", "host_is_superhost", "room_shared",
                    "room_private", "multi", "biz", "realSum"]

cleaned_data_city_columns = ['city_amsterdam', 'city_athens', 'city_barcelona', 'city_berlin', 'city_budapest', 'city_lisbon', 'city_london', 'city_paris', 'city_rome',
                             'city_vienna']

df = df_raw

app = dash.Dash(__name__)


app.layout = generate_layout(df)


@app.callback(
    [Output('graph1', 'figure'), Output(
        'graph2', 'figure')],
    [Input('data-source', 'value'), Input('data-dropdown',
                                          'value'), Input('plot-dropdown', 'value')]
)
def update_graph(data_source, column, plot_type):
    if data_source == 'raw':
        df = df_raw
        fig2 = px.box(df, x="city", y=column)

    elif data_source == 'cleaned':
        df = df_cleaned
        fig2 = px.box(df, x="city", y=column)

    if plot_type == 'histogram':
        fig = px.histogram(df[column])

    elif plot_type == 'violin':
        fig = px.violin(df[column])

    return [fig, fig2]


@app.callback(
    [Output('data-dropdown', 'options'), Output('x-scatter',
                                                'options'), Output('y-scatter', 'options')],
    Input('data-source', 'value')
)
def update_dropdown_options_2(selected_value):
    if selected_value == 'raw':
        df = df_raw

    elif selected_value == 'cleaned':
        df = df_cleaned

    value = [{'label': col, 'value': col}
             for col in df.columns]
    return [value, value, value]


@app.callback(
    Output('graph3', 'figure'),
    [Input('data-source', 'value'), Input('x-scatter',
                                          'value'), Input('y-scatter', 'value')]
)
def update_graph(data_source, X_scatter, Y_scatter):

    if data_source == 'raw':
        df = df_raw

    else:
        df = df_cleaned
    fig = px.scatter(df, x=X_scatter, y=Y_scatter,
                     marginal_x="histogram", marginal_y="rug")

    return fig


if __name__ == '__main__':
    app.run(port="8049", debug=True)
