#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 10:27:37 2019

@author: divyachandran
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
#from plotly import tools
import plotly.graph_objs as go
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

def generate_table(dataframe, max_rows=5):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )



df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/titanic.csv')

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
        html.Div([
                html.H1("Titanic: Age and Survival")
                
                ],style = {
                            'textAlign' : "center"
                            }),
        html.Div([
                dcc.RadioItems(
                        id = "select-survival",
                        options = [{'label': "Survived", 'value': 1},
                                   {'label': "Dead", 'value': 0}],
                        value = 0,
                        labelStyle={'display': 'inline-block',
                            'padding': 20}
                            
                        
                    )        
                
                ],style = {
                            'textAlign' : "center",
                            }),
        dcc.Graph(id = "my-graph"),
        
        ])


@app.callback (
        dash.dependencies.Output("my-graph","figure"),
        [dash.dependencies.Input("select-survival","value")]
        )                
def update_graph(selected):
    
    dff = df[df["Survived"] == selected]
    
    trace1 = go.Histogram(
            x= dff[dff["Sex"] == "male"]["Age"],
            opacity=0.75,
            name='Male',
            #nbinsx = 20,
            xbins={
                    "size": 5}
            
            )
    trace2 = go.Histogram(
            x= dff[dff["Sex"] == "female"]["Age"],
            opacity=0.75,
            name='Female',
            #nbinsx = 20
            xbins={
                    "size": 5}
            
            
            )
    data = [trace1, trace2]
    return{
           "data": data,
            
            "layout":go.Layout (
                    bargap=0.2,
                    bargroupgap=0.1
                    #barmode='overlay',
                    )
            
            
            
            }

if __name__ == '__main__':
    app.run_server(debug=True)        
       








