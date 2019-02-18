#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 11:02:59 2019

@author: divyachandran
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv(
    'https://gist.githubusercontent.com/chriddyp/'
    'c78bf172206ce24f77d6363a2d754b59/raw/'
    'c353e8ef842413cae56ae3920b8fd78468aa4cb2/'
    'usa-agricultural-exports-2011.csv')

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1("US Agricultural Exports", style={"textAlign": "center"}),
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='product-selected1',
                options=[{'label': i.title(), 'value': i} for i in df.columns.values[2:]],
                value="poultry")],className="six columns"),
        html.Div([
            dcc.Dropdown(
                id='product-selected2',
                options=[{'label': i.title(), 'value': i} for i in df.columns.values[2:]],
                value='beef')],className="six columns"),

    ],className="row", style={
        'margin': {
            'right': 200,
            'left': 200

        },
        'padding-right': 100,
        'padding-left': 100,

    }),
    dcc.Graph(id='my-graph')

])


@app.callback(
    dash.dependencies.Output('my-graph', 'figure'),
    [dash.dependencies.Input('product-selected1', 'value'),
     dash.dependencies.Input('product-selected2', 'value')])
def update_graph(selected_product1,selected_product2):

    dff= df[(df[selected_product1] >= 50) & (df[selected_product2] >= 50)]

    trace1=go.Bar(
                x=dff['state'],
                y=dff[selected_product1],
                name= selected_product1.title(),
                marker={

                }
            )
    trace2 = go.Bar(
                x=dff['state'],
                y=dff[selected_product2],
                name=selected_product2.title(),
                marker={

                }
            )


    return {
        'data': [trace1,trace2],
        'layout': go.Layout(
            title=f'State vs Export Value:{selected_product1.title()},{selected_product2.title()}',
            xaxis={
                'title': "State",
                'titlefont': {
                    'color': 'black',
                    'size': 14},
                'tickfont': {
                    'color': 'black'

                }
            },
            yaxis={
                'title': "Export Value",
                'titlefont': {
                    'color': 'black',
                    'size': 14,

                },
                'tickfont': {
                    'color': 'black'

                }
            }

        )

    }

server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)


# TODO: ask sham
    # keep this or previous

    # filtering states
    # more styling

