#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 10:27:37 2019

@author: divyachandran
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
# from plotly import tools
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/titanic.csv')

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
        html.H1("Titanic")

    ], style={
        'textAlign': "center"
    }),
    html.Div([
        dcc.RadioItems(
            id="select-survival",
            options=[{'label': "Survived", 'value': 1},
                     {'label': "Dead", 'value': 0}],
            value=0,
            labelStyle={'display': 'inline-block',
                        'padding': 20}
        )

    ], style={
        'textAlign': "center",
    }),
    dcc.Graph(id="my-graph"),

])


@app.callback(
    dash.dependencies.Output("my-graph", "figure"),
    [dash.dependencies.Input("select-survival", "value")]
)
def update_graph(selected):
    dff = df[df["Survived"] == selected]

    trace1 = go.Histogram(
        x=dff[dff["Sex"] == "male"]["Age"],
        opacity=0.75,
        name='Male',
        xbins={
            "size": 5}

    )
    trace2 = go.Histogram(
        x=dff[dff["Sex"] == "female"]["Age"],
        opacity=0.75,
        name='Female',
        xbins={
            "size": 5}
    )
    data = [trace1, trace2]
    return {
        "data": data,

        "layout": go.Layout(
            title=f"Male/Female Survival",
            xaxis={
                "title":"Age"
            },
            yaxis={
                "title": "Count"
            },
            bargap=0.2,
            bargroupgap=0.1,
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)
