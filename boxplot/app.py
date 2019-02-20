import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/Emissions%20Data.csv')

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
        html.H1("World Emission")
    ], style={"textAlign": "center"}),
    html.Div([
        dcc.Dropdown(
            id="selected-continent",
            options=[{
                "label": i, "value": i
            } for i in df.Year.unique()],
            value=2009,

        )], style={
        "display": "block",
        "margin-left": "auto",
        "margin-right": "auto",
        "width": "60%"

    }
    ),
    dcc.Graph(id="my-graph")

], className="container")


@app.callback(
    Output('my-graph', 'figure'),
    [Input('selected-continent', 'value')])
def update_figure(selected):
    dff = df[df["Year"] == selected]
    traces = []
    for continent in dff.Continent.unique():
        traces.append(go.Box(
            y=dff[dff["Continent"] == continent]["Emission"],
            name=continent,
            marker={"size": 4}

        ))

    return {

        "data": traces,
        "layout": go.Layout(
            title=f"Emission for {selected}",
            autosize=True,
            margin={"l": 200, "b": 100, "r": 200},
            yaxis={
                "title": f"Emission value for {selected}",
                "type": "log",
            },

        )

    }


server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
