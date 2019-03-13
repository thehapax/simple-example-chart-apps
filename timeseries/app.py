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
df['Date'] = pd.to_datetime(df.Date, infer_datetime_format=True)

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1('Stock Ticker', style={'textAlign': 'center'}),
    dcc.Dropdown(
        id='my-dropdown',
        options=[
            {'label': 'Tesla', 'value': 'TSLA'},
            {'label': 'Apple', 'value': 'AAPL'},
            {'label': 'Coke', 'value': 'COKE'},
        ],
        multi=True,
        value=['TSLA'],
        style={
            "display": "block",
            "margin-left": "auto",
            "margin-right": "auto",
            "width": "60%",
        }
    ),
    dcc.Graph(id='my-graph')
], className="container")


@app.callback(Output('my-graph', 'figure'),
              [Input('my-dropdown', 'value')])
def update_graph(selected_dropdown_value):
    dropdown = {
        "TSLA": "Tesla",
        "AAPL": "Apple",
        "COKE": "Coke",
    }
    trace1 = []
    trace2 = []
    for stock in selected_dropdown_value:
        trace1.append(go.Scatter(
            x=df[df["Stock"] == stock]["Date"],
            y=df[df["Stock"] == stock]["Open"],
            mode='lines',
            opacity=0.7,
            name=f'Open {dropdown[stock]}',
            textposition='bottom center',
            line={'color': '#ff0000'}
        ))
        trace2.append(go.Scatter(
            x=df[df["Stock"] == stock]["Date"],
            y=df[df["Stock"] == stock]["Close"],
            mode='lines',
            opacity=0.7,
            name= f'Close {dropdown[stock]}',
            textposition='bottom center', line={'color': '#9933ff'}
        ))

    traces = [trace1,trace2]
    data = [val for sublist in traces for val in sublist]
    figure = {
        'data': data,
        'layout': go.Layout(
            height=600,
            title=f"{','.join(str(dropdown[i]) for i in selected_dropdown_value)} Stock Values vs Time",
            xaxis={'rangeselector': {'buttons': list([
                {'count': 1, 'label': '1M', 'step': 'month', 'stepmode': 'backward'},
                {'count': 6, 'label': '6M', 'step': 'month', 'stepmode': 'backward'},
                {'step': 'all'}
            ])}, 'rangeslider': {'visible': True}, 'type': 'date'}
        )

    }
    return figure


server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
