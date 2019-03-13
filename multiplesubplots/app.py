#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 15:38:16 2019

@author: divyachandran
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/mtcars.csv')
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([html.H1("Car Performance Subplots")], style={"textAlign": "center"}),
    html.Div([
        html.Div([
            html.Div([
                html.H6("Scatterplot X-axis"),
                dcc.Dropdown(id="xaxis",
                             options=[{'label': "Miles/(US) gallon", 'value': "mpg"},
                                      {'label': "Displacement (cu.in.)", 'value': "disp"},
                                      {'label': "Rear axle ratio", 'value': "drat"},
                                      {'label': "Weight (1000 lbs)", 'value': "wt"},
                                      {'label': "1/4 mile time", 'value': "qsec"}],
                             value='disp',
                             style={
                                 "disply": "block",
                                 "width": "80%",
                                 "margin-left": "auto",
                                 "margin-right": "auto"
                             }
                             )]),
            html.Div([
                html.H6("Scatterplot Y-axis"),
                dcc.Dropdown(id="yaxis",
                             options=[{'label': "Miles/(US) gallon", 'value': "mpg"},
                                      {'label': "Displacement (cu.in.)", 'value': "disp"},
                                      {'label': "Rear axle ratio", 'value': "drat"},
                                      {'label': "Weight (1000 lbs)", 'value': "wt"},
                                      {'label': "1/4 mile time", 'value': "qsec"}],
                             value='mpg',
                             style={
                                 "disply": "block",
                                 "width": "80%",
                                 "margin-left": "auto",
                                 "margin-right": "auto"
                             }
                             )]),
        ], style={'width': '48%', 'display': 'inline-block'}, className="columns"),
        html.Div([
            html.H6("Box Plot, select type"),
            dcc.RadioItems(id="select-value",
                           options=[{'label': "Transmission", 'value': "am"}, {'label': "Engine-Type", 'value': "vs"}],
                           value='vs',
                           labelStyle={'display': 'inline-block'},

                           )
        ], style={'width': '48%', 'float': 'right', 'display': 'inline-block', "margin-left": "auto",
                  "margin-right": "auto"}, className="columns")
    ], className="row"),
    html.Div([
        dcc.Graph(id="my-graph")]),

], className="container")


@app.callback(
    dash.dependencies.Output("my-graph", "figure"),
    [dash.dependencies.Input("xaxis", "value"),
     dash.dependencies.Input("yaxis", "value"),
     dash.dependencies.Input("select-value", "value")]
)
def update_graph(selected1, selected2, selected3):
    trace1 = [go.Scatter(
        x=df[selected1],
        y=df[selected2],
        text=df['manufacturer'],
        mode='markers',
        opacity=0.7,
        marker={
            'size': 15,
            "color": "#00CC94",
            'line': {'width': 0.5, 'color': 'white'}
        },
        showlegend=False,

    )]

    trace2 = [go.Box(
        x=df[selected3],
        y=df['mpg'],
        name=f'{"Transmission" if selected3 == "am" else "Engine Type"}',
        xaxis='x2',
        yaxis='y2',
        marker={
            "color": "#4CEB00",
        }

    )]
    trace3 = [go.Bar(
        x=df['manufacturer'],
        y=df['hp'],
        xaxis='x3',
        yaxis='y3',
        showlegend=False,
        marker={"color": "#1166CC", "opacity": 0.7}
    )]

    trace = trace1 + trace2 + trace3
    text = {"mpg": "Miles/(US) gallon", "disp": "Displacement (cu.in.)", "drat": "Rear axle ratio",
            "qsec": "1/4 mile time", "wt": "Weight (1000 lbs)"}
    return {

        "data": trace,
        "layout": go.Layout(
            height=600,
            annotations=[
                {
                    "x": 0.07,
                    "y": 1,
                    "xref": "paper",
                    "yref": "paper",
                    "text": f'{text[selected2]} vs {text[selected1]}',
                    "showarrow": False,
                    "font": {
                        "size": 12
                    }
                },
                {
                    "x": 0.8,
                    "y": 1,
                    "xref": "paper",
                    "yref": "paper",
                    "text": f'{"Transmission" if selected3 == "am" else "Engine Type"}',
                    "showarrow": False,
                    "font": {
                        "size": 12
                    }
                },
                {
                    "x": 0.5,
                    "y": 0.4,
                    "xref": "paper",
                    "yref": "paper",
                    "text": f'Gross Horsepower Vs Manufacturer',
                    "showarrow": False,
                    "font": {
                        "size": 12
                    }
                },
            ],
            xaxis={
                "title": text[selected1],
                "domain": [0, 0.40], "anchor": 'y',

            },
            yaxis={
                "title": text[selected2],
                "domain": [0.65, 1], "anchor": 'x'
            },
            xaxis2={
                "title": f'{"Automatic transmission   Manual transmission " if selected3 == "am" else "V-shaped engine   Straight engine"}',
                "domain": [0.60, 1], "anchor": 'y2'
            },
            yaxis2={
                "title": "MilesPerGallon(mpg)",
                "domain": [0.65, 1],
                "anchor": 'x2'
            },
            xaxis3={
                "tickangle": -38,
                "domain": [0, 1], "anchor": 'y3'
            },
            yaxis3={
                "title": "Gross Horsepower(hp)",
                "domain": [0, 0.50], "anchor": 'x3'
            }
        )

    }


if __name__ == '__main__':
    app.run_server(debug=True)

# TODO: add titles in the layout
