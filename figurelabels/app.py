import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/nz_weather.csv')

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
        html.H1("Weather Record")

    ], style={
        'textAlign': "center"
    }),
    html.Div(
        dcc.Dropdown(
            id="selected-city",
            options=[{
                "label": i, "value": i
            } for i in df.columns.values[1:]],
            value=["Auckland"],
            multi=True,

        ), style={
            "display": "block",
            "margin-left": "auto",
            "margin-right": "auto",
            "width": "70%"

        }

    ),
    dcc.Graph(id="my-graph")

],className="container")


@app.callback(
    Output('my-graph', 'figure'),
    [Input('selected-city', 'value')])
def update_figure(selected):
    trace = []
    for city in selected:
        trace.append(go.Scatter(
            x=df["DATE"],
            y=df[city],
            name=city,
            mode='markers',
            marker={'size': 8,
                    "opacity": 0.6,
                    "line": {'width': 1}}, ))

    return {
        "data": trace,

        "layout": go.Layout(
            title=f"Weather:{selected}",
            xaxis={
                'title': 'DATE',
                'titlefont': {'family': 'Courier New, monospace', 'size': 18, 'color': '#0000b3'}},
            yaxis={'title': 'WEATHER',
                   'titlefont': {'family': 'Courier New, monospace', 'size': 18, 'color': '#0000b3'}}
        )

    }


server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
