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
server = app.server


df = pd.read_csv(
    'https://gist.githubusercontent.com/chriddyp/'
    'c78bf172206ce24f77d6363a2d754b59/raw/'
    'c353e8ef842413cae56ae3920b8fd78468aa4cb2/'
    'usa-agricultural-exports-2011.csv')



app.layout = html.Div([
    html.H1("US Agricultural Exports", style={"textAlign": "center"}),
    html.Div([
        dcc.Dropdown(
            id='product-selected',
            options=[{'label': i.title(), 'value': i} for i in df.columns.values[2:]],
            value="poultry")
    ], style={
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
    [dash.dependencies.Input('product-selected', 'value')])
def update_graph(selected_product):

    dff = df[df[selected_product] >= 50]
    return {
        'data': [
            go.Bar(
                x=dff['state'],
                y=dff[selected_product],

                marker={

                }
            )

        ],
        'layout': go.Layout(
            title=f'State vs {selected_product.title()}.',
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
                'title': selected_product.title(),
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


if __name__ == '__main__':
    app.run_server(debug=True)


