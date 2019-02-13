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

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/tips.csv')

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
        html.H1("TIP AMOUNT"),
        dcc.RadioItems(
            id='gender-selected',
            options=[{'label': i, 'value': i} for i in df["sex"].unique()],
            value="Female",
            labelStyle={'display': 'inline-block',
                        'padding': 20}
        )

    ], style={
        'textAlign': "center"
    }),
    dcc.Graph(id="my-graph"),

])


@app.callback(
    dash.dependencies.Output("my-graph", "figure"),
    [dash.dependencies.Input("gender-selected", "value")]
)
def update_graph(selected):
    dff = df.groupby(["day", "sex"]).mean().reset_index()
    return {
        "data": [go.Pie(
            labels=dff["day"].unique().tolist(),
            values=dff[dff["sex"] == selected]["size"].tolist(),

        )
        ],
        "layout": go.Layout(
            title='Tip amount'
        )

    }


if __name__ == '__main__':
    app.run_server(debug=True)
