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
from dash.dependencies import Input, Output, State

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/styled-line.csv')
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
        html.H1("Temperatures in New York")
    ], style={'textAlign': "center"}),
    html.Div([
        html.Div([
            dcc.RadioItems(
                id="select-text",
                options=[
                    {'label': 'Add annotations', 'value': 1},
                    {'label': 'Remove annotations', 'value': 0}
                ],
                value=1,
                labelStyle={'display': 'inline-block', "padding": 5})
        ], className="six columns"),

        html.Div([dcc.Dropdown(
            id='value-selected',
            options=[{"label": i, 'value': i} for i in df.columns[1:]],
            value=['High 2007', 'Low 2000'],
            multi=True

        )
        ], className="six columns")

    ], className="row"),

    dcc.Graph(id="my-graph"),

    html.Div([
        dcc.Input(id='x-input', type='text', placeholder="Input month", value=''),
        dcc.Input(id='y-input', type='number', placeholder="Input temperature", value=''),
        dcc.Input(id='text-input', type='text', placeholder="Input text", value=''),
        html.Button(id='submit-button', children="Type text/position & Submit"),

    ], style={"display": "block",
              "margin-left": "auto",
              "margin-right": "auto",
              "width": "60%",
              "padding": 20
              }),
], className="container")


@app.callback(
    Output("my-graph", "figure"),
    [Input("value-selected", "value"),
     Input("select-text", "value"),
     Input('submit-button', 'n_clicks')],
    [State('x-input', 'value'),
     State('y-input', 'value'),
     State('text-input', 'value')]

)
def update_graph(selected, add_text, n_clicks, x_value, y_value, text):
    dropdown ={
        "High 2014" : "High Temperature in 2014",
        "Low 2014": "Low Temperature in 2014",
        "High 2007": "High Temperature in 2007",
        "Low 2007": "Low Temperature in 2007",
        "High 2000": "High Temperature in 2000",
        "Low 2000": "Low Temperature in 2000"
    }


    trace = []
    for value in selected:
        trace.append(go.Scatter(
            x=df["Months"],
            y=df[value],
            mode="lines+markers",
            marker={
                "opacity": 0.7,
                'size': 5,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=dropdown[value]
        ))
    layout = go.Layout(
        colorway=["#EF533B", "#EF963B", "#287D95", "#2CB154", "#8C299D", "#8DD936"],
        title="Temperature Over the Months",
        yaxis={
            "title": f"Temperature (degrees F)",
        },
        xaxis={
            "title": "Months"}
    )

    figure = {
        "data": trace,
        "layout": layout}

    if add_text == 1:
        layout.update({
            "annotations": [
                {'x': x_value.title(),
                 'y': y_value,
                 'xref': 'x',
                 'yref': 'y',
                 'text': text,
                 'showarrow': False,
                 'align': 'center',
                 }
            ],
        })
        return figure

    else:
        return figure


server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)

# TODO:add more annotations with same input.
