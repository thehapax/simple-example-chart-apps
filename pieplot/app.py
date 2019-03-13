#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 14:24:07 2019

@author: divyachandran
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_ebola.csv')
df = df.dropna(axis=0)

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
        html.H1("Ebola Cases-2014")], style={"textAlign": "center"}),
    dcc.Graph(id="my-graph"),
    html.Div([dcc.Slider(
        id='month-selected',
        min=df["Month"].min(),
        max=df["Month"].max(),
        marks={i: 'Month {}'.format(i) for i in range(3, 12)},
        value=8)
    ], style={
        'textAlign': "center", "margin": "30px", "padding": "10px"}),

], className="container")


@app.callback(
    dash.dependencies.Output("my-graph", "figure"),
    [dash.dependencies.Input("month-selected", "value")]
)
def update_graph(selected):
    return {
        "data": [go.Pie(
            labels=df["Country"].unique().tolist(),
            values=df[df["Month"] == selected]["Value"].tolist(),
            marker={'colors': ['#A760F3',
                               '#F454DB',
                               '#DAFD57',
                               '#FFF457',
                               '#57D4F1']},
            textinfo='label'

        )
        ],
        "layout": go.Layout(
            title=f'Cases reported monthly',
            margin={"l": 300, "r": 300, },
        )

    }


server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
