#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 14:07:46 2019

@author: divyachandran
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
#from plotly import tools
import plotly.graph_objs as go
import pandas as pd
#from dash.dependencies import Input, Output


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/Wage%20Rigidity%20Dataset.csv')

df['year'] = pd.DatetimeIndex(df['Date']).year
df = df.dropna(how='any', axis=0)


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
        html.Div([
               html.H1("Wage Rigidity") 
                
                
                ]),
        html.Div(
              dcc.Graph(id="my-graph")  
     
                ),
        html.Div([
                dcc.Slider(
                        id='year-slider',
                        min=df['year'].min(),
                        max=df['year'].max(),
                        value= 2000,
                        marks={str(year): str(year) for year in df['year'].unique()}
                        )
                
                ])
        
        ])
@app.callback(
    dash.dependencies.Output('my-graph', 'figure'),
    [dash.dependencies.Input('year-slider', 'value')])
def update_figure(selected_year):
    dff = df[df.year == selected_year]
    
    trace1 = go.Scatter(
                y = dff["Hourly workers"],
                x = dff["Date"],
                mode='lines+markers',
                name="Hourly"
            
            )
    trace2 = go.Scatter(
                y = dff['Non-hourly workers'],
                x = dff["Date"],
                mode='markers',
                name="Non-Hourly"
            
            )
    trace3 = go.Scatter(
                y = dff["High school"],
                x = dff["Date"],
                mode='lines',
                name="High school"
            
            )
    trace4 = go.Scatter(
                y = dff["Construction"],
                x = dff["Date"],
                mode='lines+markers',
                name="Construction"
            
            )
    trace5 = go.Scatter(
                y = dff["Finance"],
                x = dff["Date"],
                mode='lines', name="Finance"
            
            )
    trace6 = go.Scatter(
                y = dff["Manufacturing"],
                x = dff["Date"],
                mode='markers', name="Manufacturing"
            
            )
    data =[trace1,trace2,trace3,trace4,trace5,trace6]
    
    return{
        "data":data,
        "layout": go.Layout(
                        
                  margin={'l': 120, 'b': 40, 't': 10, 'r': 120}
            
                )
            
           
            
            }
    
if __name__ == '__main__':
    app.run_server(debug=True)       
    
    
    
    
    
    
         