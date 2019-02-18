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

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/Emissions%20Data.csv')
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
        html.H1("Emissions"),
        dcc.Dropdown(
            id='year-selected',
            options=[{'label': i, 'value': i} for i in df["Year"].unique()],
            value=[2008],
            multi=True,
            style={
                "display": "block",
                "margin-left": "auto",
                "margin-right": "auto",
                "width" : "50%"

            }

        )

    ], style={
        'textAlign': "center"
    }),
    dcc.Graph(id="my-graph"),

])


@app.callback(
    dash.dependencies.Output("my-graph", "figure"),
    [dash.dependencies.Input("year-selected", "value")]
)
def update_graph(selected):
    trace = []
    for year in selected:
        dff = df[df["Year"] == year]
        df1 = dff.groupby(["Continent"]).mean().reset_index()
        trace.append(go.Scatter(
            x=df1["Continent"],
            y=df1["Emission"],
            name=year,
            mode="lines+markers",
            marker={
                "opacity":0.7,
                'size': 10,
                'line': {'width': 0.5, 'color': 'white'}
            },
        ))

    return {
        "data": trace,
        "layout": go.Layout(
            annotations=[
                {'x': 1, 'y': 7.5, 'xref': 'x', 'yref': 'y', 'text': 'Max=Asia', 'showarrow': True, 'font': dict(
                    family='Courier New, monospace',
                    size=16,
                    color='#ffffff'
                ), 'align': 'center', 'arrowhead': 2, 'arrowsize': 1, 'arrowwidth': 2, 'arrowcolor': '#636363',
                 'ax': 20, 'ay': -30, 'bordercolor': '#ff6666', 'borderwidth': 2, 'borderpad': 4, 'bgcolor': '#ff6666',
                 'opacity': 0.8}
            ],
            yaxis={
                "range": [0,8],
                "tick0": 0,
                "dtick": 1,
                "showgrid": False,
                "showticklabels": False,
            },
            xaxis={'showgrid': False}
        )

    }


if __name__ == '__main__':
    app.run_server(debug=True)
