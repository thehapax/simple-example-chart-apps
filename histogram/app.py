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
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/titanic.csv')

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
        html.H1("TITANIC")

    ], style={
        'textAlign': "center", 'padding': 10
    }),
    html.Div([
        dcc.RadioItems(
            id="select-survival",
            options=[{'label': "Survived", 'value': 1},
                     {'label': "Dead", 'value': 0}],
            value=0,
            labelStyle={'display': 'inline-block',
                        'padding': 10}
        )

    ], style={
        'textAlign': "center",
    }),
    html.Div([
        html.Div([
            dcc.Graph(id="scatter-graph",
                      hoverData={'points': [{'customdata': '30'}]})], className="six columns"),
        html.Div([
            dcc.Graph(id="hist-graph",clear_on_unhover=True,)],className="six columns"),
    ]),
], className="container")


@app.callback(
    dash.dependencies.Output("scatter-graph", "figure"),
    [dash.dependencies.Input("select-survival", "value"),
     dash.dependencies.Input("hist-graph", "hoverData")]
)
def update_scatter(selected, hoverdata):
    dff = df[df["Survived"] == selected]
    trace = []
    for sex in dff["Sex"].unique():
        trace.append(go.Scatter(
            x=dff[dff["Sex"] == sex]["Age"],
            y=dff[dff["Sex"] == sex]["Fare"],
            mode="markers",
            name=sex.title(),
            customdata=dff[dff["Sex"] == sex]["Age"],
            marker={
                "size": 10
            }
        ))

    layout = go.Layout(
        title=f"Fare vs Age",
        colorway = ["#7603F1", "#F200CC"],
        hovermode='closest',
        xaxis={
            "title": "Age",
            "range": [0, 75],
            "tick0": 0,
            "dtick": 5,
            "showgrid": False
        },
        yaxis={
            "title": "Fare",
            "range": [-30, 300],
            "tick0": 0,
            "dtick": 25,
            "showgrid": False
        },

    )
    figure1 = {
        "data": trace,

        "layout": layout
    }

    if hoverdata is not None:
        age = hoverdata["points"][0]['x']
        size1 = []
        for i in dff[dff["Sex"] == "male"]["Age"]:
            if i == round(age):
                size1.append(30)
            else:
                size1.append(10)
        size2=[]
        for i in dff[dff["Sex"] == "female"]["Age"]:
            if i == round(age):
                size2.append(30)
            else:
                size2.append(10)
        # noinspection PyTypeChecker
        figure1["data"][0].update(go.Scatter
                        (marker={"size": size1, "opacity": 1}))
        # noinspection PyTypeChecker
        figure1["data"][1].update(go.Scatter
                                  (marker={"size": size2, "opacity": 1}))


    return figure1


@app.callback(
    dash.dependencies.Output("hist-graph", "figure"),
    [dash.dependencies.Input("select-survival", "value"),
     dash.dependencies.Input('scatter-graph', 'hoverData'),
     ]
)
def update_graph(selected, hoverdata1):
    dff = df[df["Survived"] == selected]
    age = hoverdata1["points"][0]['customdata']
    trace = go.Histogram(
        x=dff["Age"],
        opacity=0.7,
        name="Male",
        xbins={
            "size": 5},
        customdata=dff["Age"],


    )
    layout = go.Layout(
        title=f"Age Distribution",
        xaxis={
            "title": "Age",
            "showgrid": False
        },
        yaxis={
            "title": "Count",
            "showgrid": False
        },

    )
    figure2 = {"data": [trace], "layout": layout}

    def create_bins(lower_bound, width, quantity):
        bins = []
        for low in range(lower_bound,
                         lower_bound + quantity * width + 1, width):
            bins.append((low, low + width))
        return bins

    bins = create_bins(lower_bound=0,
                       width=5,
                       quantity=20)

    def find_bin(value, bins):
        for i in range(0, len(bins)):
            if bins[i][0] <= value < bins[i][1]:
                return i
        return -1

    if hoverdata1 is not None:
        color = []
        for i in range(0, len(bins)):
            if bins[i] == bins[find_bin(float(age), bins)]:
                color.append("#C7FD00")
            else:
                color.append("#7603F1")
        # noinspection PyTypeChecker
        figure2["data"][0].update(go.Histogram
                                  (marker={"color": color}))

    return figure2


server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)

# todo: hover from hist on scatter, not hovering after bin 45
