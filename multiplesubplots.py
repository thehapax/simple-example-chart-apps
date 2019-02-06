#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 15:38:16 2019

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



df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/Antibiotics.csv')

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
        html.Div([
                html.H1("Antibiotic Effectiveness"),
                dcc.RadioItems(
                id='bacteria-type',
                options=[{'label': i, 'value': i} for i in df[' Gram'].unique()],
                value='positive',
                labelStyle={'display': 'inline-block',
                            'padding': 20}
                            )
                
                ],style = {
                            'textAlign' : "center"
                            }),
    
              
           dcc.Graph(id="my-graph"), 
           
           html.Div([
                   #generate_table(df)
                   
                   ],style = {
                            "position": "absolute",
                             "top": "60%" ,
                             "left": "30%",
                             
                             #"margin": {"l": -100px ,"b":0 ,"t":0 ,"r":-150px },
                            'textAlign' : "center"
                            }),
           
 
               
                ])
        
@app.callback(
        dash.dependencies.Output("my-graph","figure"),
        [dash.dependencies.Input("bacteria-type","value")]
        ) 
def update_graph(selected) :
    dff = df[df[' Gram']== selected]
    
    trace1 = go.Bar(
                  x=dff["Bacteria"],
                  y=dff[" Penicillin"],
                  name = "Penicillin",
                  )
    trace2 = go.Bar(
                  x=dff["Bacteria"],
                  y=dff[" Streptomycin"],
                  xaxis='x2',
                  name = "Streptomycin"
                  
                  
                  )
    trace3 = go.Bar(
                  x=dff["Bacteria"],
                  y=dff[" Neomycin"],
                  xaxis='x3',
                  name = "Neomycin"
                  )
    
    
    data = [trace1, trace2, trace3]
    
    return {
          "data" : data,
        "layout" : go.Layout(
                         
                  margin={'l': 80, 'b': 120, 't': 30, 'r': 80},
                  xaxis={"domain":[0, 0.30]},
                  yaxis={"domain":[0, 1],
                         "tickangle" : 45,
                         "title": "Minimum Inhibitory Concentration(mcg/ml)" ,
                         "type":'log',
                         #"autorange": "reversed"
                        
                         },
                  xaxis2={"domain":[0.35, 0.65]},
                          
                  xaxis3={"domain":[0.70, 1],
                          
                          },     
                    
                          
                  )
            
            }          
      
if __name__ == '__main__':
    app.run_server(debug=True)        
       