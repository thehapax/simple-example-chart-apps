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
# from plotly import tools
import plotly.graph_objs as go

# from dash.dependencies import Input, Output

external_stylesheets = ['https://raw.githubusercontent.com/plotly/dash-app-stylesheets/master/dash-docs-base.css']

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_ebola.csv')
df = df.fillna(method='ffill')

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
        html.H1("Ebola Cases-2014"),
        html.Div([dcc.Dropdown(
            id='month-selected',
            options=[{'label': f"Month: {i}", 'value': i} for i in df["Month"].unique()],
            value=8,

        )], style={
            'margin': {
                'right': 200,
                'left': 200

            },
            'padding-right': 500,
            'padding-left': 500,

        })

    ], style={
        'textAlign': "center"
    }),
    dcc.Graph(id="my-graph"),

], className="container", style={"margin": "30px", "padding": "20px"})


@app.callback(
    dash.dependencies.Output("my-graph", "figure"),
    [dash.dependencies.Input("month-selected", "value")]
)
def update_graph(selected):
    return {
        "data": [go.Pie(
            labels=df["Country"].unique().tolist(),
            values=df[df["Month"] == selected]["Value"].tolist(),
            marker={'colors': ['rgb(33, 75, 99)',
                               'rgb(79, 129, 102)',
                               'rgb(151, 179, 100)',
                               'rgb(175, 49, 35)',
                               'rgb(36, 73, 147)']},
            textinfo='label'

        )
        ],
        "layout": go.Layout(
            title=f'Ebola cases reported in {selected}th month',
            # width = 1000,
            margin={"l": 300, "r": 300, },
        )

    }


server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
