import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2016-weather-data-seattle.csv')
df = df.dropna()
df["Date"] = pd.to_datetime(df["Date"])
df["year"] = df["Date"].dt.year

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
        html.H1("Weather Records for Seattle")

    ], style={
        'textAlign': "center"
    }),
    html.Div([
        dcc.Dropdown(
            id="selected-value",
            options=[
                {"label": "Maximum Temperature", "value": "Max_TemperatureC"},
                {"label": "Mean Temperature", "value": "Mean_TemperatureC"},
                {"label": "Minimum Temperature", "value": "Min_TemperatureC"},
            ],
            multi=True,
            value=["Mean_TemperatureC"], )
    ],className="row",style={"display":"block","width":"60%","margin-left":"auto","margin-right":"auto"}),
    html.Div([
        dcc.Graph(id="my-graph")]),
    html.Div([
        dcc.RangeSlider(id="year-range",
                        min=1948,
                        max=2015,
                        step=1,
                        marks={"1948": 1948,
                               "1954": 1954,
                               "1966": 1966,
                               "1975": 1975,
                               "1983": 1983,
                               "1994": 1994,
                               "2000": 2000,
                               "2005": 2005,
                               "2010": 2010,
                               "2012": 2012,
                               "2015": 2015
                               },
                        value=[1998, 2000]
                        )
    ])

], className="container")


@app.callback(
    Output('my-graph', 'figure'),
    [Input('selected-value', 'value'),
     Input('year-range', 'value')])
def update_figure(selected, year):
    text = {"Max_TemperatureC": "Maximum Temperature",
            "Mean_TemperatureC": "Mean Temperature",
            "Min_TemperatureC": "Minimum Temperature"}
    dff = df[(df["year"] >= year[0]) & (df["year"] <= year[1])]

    trace = []
    for type in selected:
        trace.append(go.Scatter(
            x=dff["Date"],
            y=dff[type],
            name=text[type],
            mode='lines',
            marker={'size': 8, "opacity": 0.6,
                    "line": {'width': 0.5}}, ))

    return {
        "data": trace,

        "layout": go.Layout(
            title="Temperature Variations Over Time",
            yaxis={
                "title": "Temperature ( degree celsius )",
            },
            xaxis={
                "title": "Date"},
            colorway=['#fdae61', '#abd9e9', '#2c7bb6']
        )

    }


if __name__ == '__main__':
    app.run_server(debug=True)
