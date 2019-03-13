#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 14:07:46 2019

@author: divyachandran
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/Wage%20Rigidity%20Dataset.csv')
df.dropna(inplace=True)

df['year'] = pd.DatetimeIndex(df['Date']).year

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
        html.H1("Employment wage data")

    ], style={"text-align": "center"}),
    html.Div(
        dcc.Graph(id="my-graph")

    ),
    html.Div([
        dcc.RangeSlider(
            id='year-slider',
            min=1983,
            max=df['year'].max(),
            marks={
                1983: '1983',
                1990: '1990',
                2000: '2000',
                2003: '2003',
                2005: '2005',
                2008: '2008',
                2010: '2010',
                2013: '2013',
                2016: '2016'
            },
            value=[2000, 2005]
        )

    ], style={"margin": 20, "padding": 30})

], className="container")


@app.callback(
    dash.dependencies.Output('my-graph', 'figure'),
    [dash.dependencies.Input('year-slider', 'value')])
def update_figure(selected_year):
    pd.options.mode.chained_assignment = None  # default='SettingWithCopyWarning'
    dff = df[(df.year >= selected_year[0]) & (df.year <= selected_year[1])]
    dff['Date'] = pd.to_datetime(dff['Date']).dt.strftime('%y/%d')
    trace1 = go.Scatter(
        y=dff["Hourly workers"],
        x=dff["Date"],
        mode='lines+markers',
        marker={"size": 4},
        name="Hourly"

    )
    trace2 = go.Scatter(
        y=dff['Non-hourly workers'],
        x=dff["Date"],
        mode='markers',
        marker={"size": 4},
        name="Non-Hourly"

    )
    trace3 = go.Scatter(
        y=dff["High school"],
        x=dff["Date"],
        mode='lines',
        marker={"size": 4},
        name="High school"

    )
    trace4 = go.Scatter(
        y=dff["Construction"],
        x=dff["Date"],
        mode='lines+markers',
        marker={"size": 4},
        name="Construction"

    )
    trace5 = go.Scatter(
        y=dff["Finance"],
        x=dff["Date"],
        mode='lines',
        marker={"size": 4},
        name="Finance"

    )
    trace6 = go.Scatter(
        y=dff["Manufacturing"],
        x=dff["Date"],
        mode='markers',
        marker={"size": 4},
        name="Manufacturing"

    )
    data = [trace1, trace2, trace3, trace4, trace5, trace6]

    return {
        "data": data,
        "layout": go.Layout(
            title="Wages in different employment sector vs time",
            xaxis={
                "title": f"For the year {'-'.join(str(i)for i in selected_year)}",
                "tickangle": 45,
            },
            yaxis={
                "title": "Wages",
                "range": [0, 25],
                "tick0": 0,
                "dtick": 5,
            },

        )

    }


server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
