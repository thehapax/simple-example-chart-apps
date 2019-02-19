#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 15:29:02 2019

@author: divyachandran
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/hello-world-stock.csv')
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1('Stock Ticker', style={'textAlign': 'center'}),
    dcc.Dropdown(
        id='my-dropdown',
        options=[
            {'label': 'Tesla', 'value': 'TSLA'},
            {'label': 'Apple', 'value': 'AAPL'},
            {'label': 'Coke', 'value': 'COKE'}
        ],
        value='TSLA'
    ),
    dcc.Graph(id='my-graph')
], className="container")


@app.callback(Output('my-graph', 'figure'),
              [Input('my-dropdown', 'value')])
def update_graph(selected_dropdown_value):
    dff = df[df['Stock'] == selected_dropdown_value]
    trace1 = go.Scatter(
        x=dff.Date,
        y=dff.Open,
        mode='lines',
        opacity=0.7,
        name="Open",
        textposition='bottom center',
        line={'color': '#ff0000'}
    )

    trace2 = go.Scatter(
        x=dff.Date,
        y=dff.Close,
        mode='lines',
        opacity=0.7,
        name="Close",
        textposition='bottom center', line={'color': '#9933ff'}
    )

    data = [trace1, trace2]

    return {
        'data': data,
        'layout': go.Layout(
            title=f'Stock Values for {selected_dropdown_value}',
            xaxis={'rangeselector': {'buttons': list([
                {'count': 1, 'label': '1m', 'step': 'month', 'stepmode': 'backward'},
                {'count': 6, 'label': '6m', 'step': 'month', 'stepmode': 'backward'},
                {'step': 'all'}
            ])}, 'rangeslider': {'visible': True}, 'type': 'date'}
        )

    }


server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
