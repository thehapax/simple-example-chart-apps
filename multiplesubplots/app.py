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
                html.Span("Scatterplot X-axis",className="three columns",style={"width": 150,"padding": 10,"text-align":"right" }),
                html.Div(dcc.Dropdown(id="xaxis",
                             options=[{'label': "Miles per gallon", 'value': "mpg"},
                                      {'label': "Displacement (cu.in.)", 'value': "disp"},
                                      {'label': "Rear axle ratio", 'value': "drat"},
                                      {'label': "Weight (1000 lbs)", 'value': "wt"},
                                      {'label': "1/4 mile time", 'value': "qsec"}],
                             value='disp',

                                      ),className="three columns",style={"width": 250,"margin":0})],className="row"),
            html.Div([
                html.Span("Scatterplot Y-axis",className="three columns",style={"width": 150,"padding": 10,"text-align":"right"}),
                html.Div(dcc.Dropdown(id="yaxis",
                             options=[{'label': "Miles per gallon", 'value': "mpg"},
                                      {'label': "Displacement (cu.in.)", 'value': "disp"},
                                      {'label': "Rear axle ratio", 'value': "drat"},
                                      {'label': "Weight (1000 lbs)", 'value': "wt"},
                                      {'label': "1/4 mile time", 'value': "qsec"}],
                             value='mpg',

                                      ),className="three columns",style={"width": 250,"margin":0})],className="row"),
        ], style={'width': '48%', 'display': 'inline-block'}, className="six columns"),
        html.Div([
            html.Div([
                html.Span("Box Plot x-axis",className="three columns",style={"text-align":"right","width":150,"padding":10}),
                html.Div(dcc.RadioItems(id="select-value",
                               options=[{'label': "Transmission", 'value': "am"},
                                        {'label': "Engine-Type", 'value': "vs"}],
                               value='vs',
                               labelStyle={'display': 'inline'},

                               ),className="three columns",style={"width":250,"margin":0,"padding": 10})], className="row"),
            html.Div([
                html.Span("Box Plot y-axis",className="three columns",style={"width": 150,"padding": 10,"text-align":"right" }),
                html.Div(dcc.Dropdown(id="boxplot-yaxis",
                             options=[{'label': "Miles per gallon", 'value': "mpg"},
                                      {'label': "Displacement (cu.in.)", 'value': "disp"},
                                      {'label': "Rear axle ratio", 'value': "drat"},
                                      {'label': "Weight (1000 lbs)", 'value': "wt"},
                                      {'label': "1/4 mile time", 'value': "qsec"}],
                             value='mpg',
              ) ,className="three columns",style={"width": 250,"margin":0})
            ], className="row")
        ], style={'width': '48%', 'float': 'right', 'display': 'inline-block', "margin-left": "auto",
                  "margin-right": "auto"}, className="six columns")
    ], className="row"),
    html.Div([
        dcc.Graph(id="my-graph")]),

], className="container")


@app.callback(
    dash.dependencies.Output("my-graph", "figure"),
    [dash.dependencies.Input("xaxis", "value"),
     dash.dependencies.Input("yaxis", "value"),
     dash.dependencies.Input("boxplot-yaxis", "value"),
     dash.dependencies.Input("select-value", "value")]
)
def update_graph(selected1, selected2, selected_box_y, selected_box_x):
    trace1 = [go.Scatter(
        x=df[selected1],
        y=df[selected2],
        text=df['manufacturer'],
        mode='markers',
        opacity=0.7,
        marker={
            'size': 10,
            "color": "#00CC94",

        },
        showlegend=False,

    )]

    trace2 = [go.Box(
        x=df[selected_box_x],
        y=df[selected_box_y],
        name=f'{"Transmission" if selected_box_x == "am" else "Engine Type"}',
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
        marker={"color": "#5DB4F2", "opacity": 0.8}
    )]

    trace = trace1 + trace2 + trace3
    text = {"mpg": "Miles per gallon", "disp": "Displacement (cu.in.)", "drat": "Rear axle ratio",
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
                    "x": 0.85,
                    "y": 1,
                    "xref": "paper",
                    "yref": "paper",
                    "text": f'{"Transmission" if selected_box_x == "am" else "Engine Type"}',
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
                "title": f'{"Automatic transmission   Manual transmission " if selected_box_x == "am" else "V-shaped engine   Straight engine"}',
                "domain": [0.60, 1], "anchor": 'y2',
                "showticklabels": False,

            },
            yaxis2={
                "title": text[selected_box_y],
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


server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)

# TODO: change dropdown to inline
